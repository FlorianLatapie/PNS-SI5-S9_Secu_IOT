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

package savacard;

import javacard.framework.*;
import javacard.security.KeyPair;
import javacard.security.RSAPrivateKey;
import javacard.security.RSAPublicKey;
import javacard.security.Signature;

/**
 * The class implement a smart card that can sign messages
 * It is protected by a PIN code and owns a RSA key pair.
 */
public class SavaCard extends Applet {

    public static final byte INS_DEBUG = (byte) 0x03;

    /**
     * Default PIN code
     */
    public static final byte[] DEFAULT_PIN = {0x01, 0x02, 0x03, 0x04};

    /**
     * Size of the RSA key pair
     */
    public static final short KEY_BITS = 512;

    /**
     * CLA byte of the applet
     */
    final static byte CLA = (byte) 0xB0;

    // codes of INS byte in the command APDU header

    /**
     * INS byte of the login command
     */
    final static byte INS_LOGIN = (byte) 0x01;

    /**
     * INS byte of the modify pin command
     */
    final static byte INS_MODIFY_PIN = (byte) 0x02;

    /**
     * INS byte of the sign message command
     */
    final static byte INS_SIGN_MESSAGE = (byte) 0x04;

    /**
     * INS byte of the send public key command
     */
    final static byte INS_SEND_PUBLIC_KEY = (byte) 0x05;

    /**
     * INS byte of the factory reset command
     */
    final static byte INS_FACTORY_RESET = (byte) 0x06;

    /**
     * Length of the PIN code
     */
    final static byte PIN_LENGTH = 4;

    /**
     * Maximum number of tries for the PIN code
     */
    final static byte MAX_PIN_RETRY = 3;

    /**
     * PIN object used to protect the applet
     */
    OwnerPIN pin;

    /**
     * Private key of the key pair
     */
    private RSAPrivateKey privateKey;

    /**
     * Public key of the key pair
     */
    private RSAPublicKey publicKey;


    protected SavaCard() {
        pin = new OwnerPIN(MAX_PIN_RETRY, PIN_LENGTH);
        factoryReset();
        register();
    }

    public static void install(byte[] bArray, short bOffset, byte bLength) {
        // Create the Signer applet instance
        new SavaCard();
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
            // If the applet is selected, we do nothing
            ISOException.throwIt(ISO7816.SW_NO_ERROR);
        }

        byte[] buffer = apdu.getBuffer();
        // Ensure all the incoming data has been received
        apdu.setIncomingAndReceive();

        if (buffer[ISO7816.OFFSET_CLA] != CLA) {
            // throw exception if the CLA byte is not the one expected
            ISOException.throwIt(ISO7816.SW_CLA_NOT_SUPPORTED);
        }

        // Process the command based on the INS byte
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
            case INS_DEBUG:
                debug(apdu);
                break;
        }
    }

    private void debug(APDU apdu) {
        byte[] buffer = apdu.getBuffer();
        byte[] data = {0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x20, 0x57, 0x6f, 0x72, 0x6c, 0x64, 0x20, 0x21}; // "Hello World !"
        Util.arrayCopy(data, (short) 0, buffer, ISO7816.OFFSET_CDATA, (short) data.length);
        apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (short) data.length);
    }

    /**
     * Factory reset the applet
     * Reset the PIN code to the default one and generate a new RSA key pair
     */
    private void factoryReset() {
        setDefaultPin();
        generateRSAKeys();
    }

    /**
     * Authenticate the user with the PIN code to the applet
     *
     * @param apdu data received from the terminal
     */
    private void login(APDU apdu) {
        if (pin.isValidated()) {
            ISOException.throwIt(ISO7816.SW_CONDITIONS_NOT_SATISFIED);
        }

        byte[] buffer = apdu.getBuffer();
        checkPin(buffer);
    }

    /**
     * Check if the user is authenticated
     */
    private void checkLogin() {
        if (!pin.isValidated()) {
            ISOException.throwIt(ISO7816.SW_SECURITY_STATUS_NOT_SATISFIED);
        }
    }

    /**
     * Initialize the PIN code and the RSA key pair
     */
    private void setDefaultPin() {
        pin.update(DEFAULT_PIN, (short) 0, PIN_LENGTH);
    }

    /**
     * Check if the PIN code is valid
     *
     * @param buffer data received from the terminal
     */
    private void checkPin(byte[] buffer) {
        if (buffer[ISO7816.OFFSET_LC] != PIN_LENGTH) {
            ISOException.throwIt(ISO7816.SW_WRONG_LENGTH);
        }

        if (!pin.check(buffer, ISO7816.OFFSET_CDATA, PIN_LENGTH)) {
            ISOException.throwIt(ISO7816.SW_SECURITY_STATUS_NOT_SATISFIED);
        }
    }

    /**
     * Modify the PIN code
     *
     * @param apdu data received from the terminal
     */
    private void modifyPin(APDU apdu) {
        checkLogin();
        byte[] buffer = apdu.getBuffer();

        if (buffer[ISO7816.OFFSET_LC] != PIN_LENGTH) {
            ISOException.throwIt(ISO7816.SW_WRONG_LENGTH);
        }

        pin.update(buffer, ISO7816.OFFSET_CDATA, PIN_LENGTH);
    }

    /**
     * Generate a RSA key pair used to sign messages
     */
    private void generateRSAKeys() {
        KeyPair keyPair = new KeyPair(KeyPair.ALG_RSA, KEY_BITS);
        keyPair.genKeyPair();
        privateKey = (RSAPrivateKey) keyPair.getPrivate();
        publicKey = (RSAPublicKey) keyPair.getPublic();
    }

    /**
     * Sign the fingerprint of the message with the RSA private key
     *
     * @param apdu data received from the terminal
     */
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

    /**
     * Send the public key to the terminal
     *
     * @param apdu data received from the terminal
     */
    private void sendPublicKey(APDU apdu) {
        short keyToSend = serializeKey(publicKey, apdu.getBuffer(), ISO7816.OFFSET_CDATA);
        apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, keyToSend);
    }

    /**
     * Serialize a RSA public key
     *
     * @param key    the RSA public key to serialize
     * @param buffer the buffer to write the serialized key
     * @param offset the offset to write the serialized key
     * @return the length of the serialized key
     */
    private short serializeKey(RSAPublicKey key, byte[] buffer, short offset) {
        // Code from the thread in stackoverflow :
        // https://stackoverflow.com/questions/42690733/javacard-send-rsa-public-key-in-apdu

        short expLen = key.getExponent(buffer, (short) (offset + 2));
        Util.setShort(buffer, offset, expLen);
        short modLen = key.getModulus(buffer, (short) (offset + 4 + expLen));
        Util.setShort(buffer, (short) (offset + 2 + expLen), modLen);
        return (short) (4 + expLen + modLen);
    }
}
