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

import java.security.KeyPair;
import java.security.interfaces.RSAPrivateKey;
import java.security.interfaces.RSAPublicKey;

/**
 */

public class NotreProjet extends Applet
{
    /* constants declaration */
    // code of CLA byte in the command APDU header
    final static byte SIGNER_CLA = (byte)0xB0;

    // codes of INS byte in the command APDU header
    final static byte MODIFY_PIN = (byte) 0x02;
    final static byte SIGN_MESSAGE = (byte) 0x04;
    final static byte SEND_PUBLIC_KEY = (byte) 0x05;

    final static byte PIN_LENGTH = 4;

    final static byte MAX_PIN_RETRY = 3;

    public static final byte[] DEFAULT_PIN = {0x01, 0x02, 0x03, 0x04};


    OwnerPIN pin;
    RSAPrivateKey privateKey;
    RSAPublicKey publicKey;


    /**
     * Only this class's install method should create the applet object.
     */

    protected NotreProjet() {
        pin = new OwnerPIN(MAX_PIN_RETRY, PIN_LENGTH);
        setDefaultPin();
        register();
    }
    /**
     * Installs this applet.
     * @param bArray the array containing installation parameters
     * @param bOffset the starting offset in bArray
     * @param bLength the length in bytes of the parameter data in bArray
     */
    public static void install(byte[] bArray, short bOffset, byte bLength)
    {
        // Create the Signer applet instance
        new NotreProjet();
    }

    private void setDefaultPin() {
        pin.update(DEFAULT_PIN, (short) 0, PIN_LENGTH);
    }

    private void generateRSAKeys() {
        KeyPair keyGenerator = new KeyPair(KeyPair)
    }

    /**
     * Processes an incoming APDU.
     * @see APDU
     * @param apdu the incoming APDU
     * @exception ISOException with the response bytes per ISO 7816-4
     */

    public boolean select() {
        if (pin.getTriesRemaining() == 0) return false;
        return true;
    }
    public void process(APDU apdu)
    {
        byte buffer[] = apdu.getBuffer();

        short bytesRead = apdu.setIncomingAndReceive();
        short echoOffset = (short)0;

        while ( bytesRead > 0 ) {
            Util.arrayCopyNonAtomic(buffer, ISO7816.OFFSET_CDATA, echoBytes, echoOffset, bytesRead);
            echoOffset += bytesRead;
            bytesRead = apdu.receiveBytes(ISO7816.OFFSET_CDATA);
        }

        apdu.setOutgoing();
        apdu.setOutgoingLength( (short) (echoOffset + 5) );

        // echo header
        apdu.sendBytes( (short)0, (short) 5);
        // echo data
        apdu.sendBytesLong( echoBytes, (short) 0, echoOffset );
    }

}
