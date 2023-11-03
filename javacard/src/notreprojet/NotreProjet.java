/*
 * Copyright 2005 Sun Microsystems, Inc. All rights reserved.
 * SUN PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
 */

// /*
// Workfile:@(#)HelloWorld.java	1.7
// Version:1.7
// Date:01/03/06
//
// Archive:  /Products/Europa/samples/com/sun/javacard/samples/HelloWorld/HelloWorld.java
// Modified:01/03/06 19:01:06
// Original author:  Mitch Butler
// */

package notreprojet;

import javacard.framework.*;
import javacard.security.*;

/**
 *
 */

public class NotreProjet extends Applet {
    public static final byte[] DEFAULT_PIN = {0x01, 0x02, 0x03, 0x04};
    public static final short KEY_BITS = 512;
    /* constants declaration */
    // code of CLA byte in the command APDU header
    final static byte CLA = (byte) 0xB0;
    // codes of INS byte in the command APDU header

    final static byte INS_LOGIN = (byte) 0x01;
    final static byte INS_MODIFY_PIN = (byte) 0x02;
    final static byte INS_SIGN_MESSAGE = (byte) 0x04;
    final static byte INS_SEND_PUBLIC_KEY = (byte) 0x05;

    final static byte INS_FACTORY_RESET = (byte) 0x06;
    final static byte PIN_LENGTH = 4;
    final static byte MAX_PIN_RETRY = 3;
    OwnerPIN pin;
    private KeyPair keyPair;

    private RSAPrivateKey privateKey;

    private RSAPublicKey publicKey;


    /**
     * Only this class's install method should create the applet object.
     */

    protected NotreProjet() {
        pin = new OwnerPIN(MAX_PIN_RETRY, PIN_LENGTH);
        factoryReset();
        register();
    }

    /**
     * Installs this applet.
     *
     * @param bArray  the array containing installation parameters
     * @param bOffset the starting offset in bArray
     * @param bLength the length in bytes of the parameter data in bArray
     */
    public static void install(byte[] bArray, short bOffset, byte bLength) {
        // Create the Signer applet instance
        new NotreProjet();
    }

    private void setDefaultPin() {
        pin.update(DEFAULT_PIN, (short) 0, PIN_LENGTH);
    }

    private void generateRSAKeys() {
        keyPair = new KeyPair(KeyPair.ALG_RSA, KEY_BITS);
        keyPair.genKeyPair();
        privateKey = (RSAPrivateKey) keyPair.getPrivate();
        publicKey = (RSAPublicKey) keyPair.getPublic();
    }

    public boolean select() {
        return pin.getTriesRemaining() != 0;
    }

    public void deselect() {
        checkLogin();
        pin.reset();
    }

    public void process(APDU apdu) {
        if (selectingApplet()) {
            // ignore if the applet is being selected
            ISOException.throwIt(ISO7816.SW_NO_ERROR);
        }

        byte[] buffer = apdu.getBuffer();
        apdu.setIncomingAndReceive();

        if (buffer[ISO7816.OFFSET_CLA] != CLA) {
            // throw exception if the CLA byte is not the one expected
            ISOException.throwIt(ISO7816.SW_CLA_NOT_SUPPORTED);
        }

        switch (buffer[ISO7816.OFFSET_INS]) {
            case INS_LOGIN:
                login(apdu);
                break;
            case INS_MODIFY_PIN:
                modifyPin(apdu);
                break;
            case INS_SIGN_MESSAGE:
                signMessage(apdu);
                break;
            case INS_SEND_PUBLIC_KEY:
                sendPublicKey(apdu);
                break;
            case INS_FACTORY_RESET:
                factoryReset();
                break;
        }
    }

    private void factoryReset() {
        setDefaultPin();
        generateRSAKeys();
    }

    private void login(APDU apdu) {
        if (pin.isValidated()) {
            ISOException.throwIt(ISO7816.SW_CONDITIONS_NOT_SATISFIED);
        }

        byte[] buffer = apdu.getBuffer();
        checkPin(buffer);
    }

    private void checkPin(byte[] buffer) {
        if (buffer[ISO7816.OFFSET_LC] != PIN_LENGTH) {
            ISOException.throwIt(ISO7816.SW_WRONG_LENGTH);
        }

        if (!pin.check(buffer, ISO7816.OFFSET_CDATA, PIN_LENGTH)) {
            ISOException.throwIt(ISO7816.SW_SECURITY_STATUS_NOT_SATISFIED);
        }
    }

    private void signMessage(APDU apdu) {
        checkLogin();
        byte[] buffer = apdu.getBuffer();

        if (buffer[ISO7816.OFFSET_LC] == 0) {
            ISOException.throwIt(ISO7816.SW_DATA_INVALID);
        }

        // Maybe a problem on the length of the buffer, see that later
        Signature signature = Signature.getInstance(Signature.ALG_RSA_SHA_PKCS1, false);
        signature.init(privateKey, Signature.MODE_SIGN);
        byte[] signedMessage = new byte[signature.getLength()];
        short signatureLength = signature.sign(buffer, ISO7816.OFFSET_CDATA, ISO7816.OFFSET_LC, signedMessage, (short) 0);
        Util.arrayCopy(signedMessage, (short) 0, buffer, ISO7816.OFFSET_CDATA, signatureLength);

        apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, signatureLength);

    }

    private void sendPublicKey(APDU apdu) {
        short keyToSend = serializeKey(publicKey, apdu.getBuffer(), ISO7816.OFFSET_CDATA);
        apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, keyToSend);
    }

    private short serializeKey(RSAPublicKey key, byte[] buffer, short offset) {
        // Code from the thread in stackoverflow :
        // https://stackoverflow.com/questions/42690733/javacard-send-rsa-public-key-in-apdu

        short expLen = key.getExponent(buffer, (short) (offset + 2));
        Util.setShort(buffer, offset, expLen);
        short modLen = key.getModulus(buffer, (short) (offset + 4 + expLen));
        Util.setShort(buffer, (short) (offset + 2 + expLen), modLen);
        return (short) (4 + expLen + modLen);
    }

    private void checkLogin() {
        if (!pin.isValidated()) {
            ISOException.throwIt(ISO7816.SW_SECURITY_STATUS_NOT_SATISFIED);
        }
    }

    private void modifyPin(APDU apdu) {
        checkLogin();
        byte[] buffer = apdu.getBuffer();

        if (buffer[ISO7816.OFFSET_LC] != PIN_LENGTH) {
            ISOException.throwIt(ISO7816.SW_WRONG_LENGTH);
        }

        // Comment maybe useless need more research
        apdu.setIncomingAndReceive();

        pin.update(buffer, ISO7816.OFFSET_CDATA, PIN_LENGTH);
    }
}
