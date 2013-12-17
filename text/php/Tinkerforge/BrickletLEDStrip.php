<?php

/* ***********************************************************
 * This file was automatically generated on 2013-12-06.      *
 *                                                           *
 * Bindings Version 2.0.11                                    *
 *                                                           *
 * If you have a bugfix for this file and want to commit it, *
 * please fix the bug in the generator. You can find a link  *
 * to the generator git on tinkerforge.com                   *
 *************************************************************/

namespace Tinkerforge;

require_once(__DIR__ . '/IPConnection.php');

/**
 * Device to control up to 320 RGB LEDs
 */
class BrickletLEDStrip extends Device
{

    /**
     * This callback is triggered directly after a new frame is rendered.
     *
     * You should send the data for the next frame directly after this callback
     * was triggered.
     *
     * For an explanation of the general approach see BrickletLEDStrip::setRGBValues().
     */
    const CALLBACK_FRAME_RENDERED = 6;


    /**
     * @internal
     */
    const FUNCTION_SET_RGB_VALUES = 1;

    /**
     * @internal
     */
    const FUNCTION_GET_RGB_VALUES = 2;

    /**
     * @internal
     */
    const FUNCTION_SET_FRAME_DURATION = 3;

    /**
     * @internal
     */
    const FUNCTION_GET_FRAME_DURATION = 4;

    /**
     * @internal
     */
    const FUNCTION_GET_SUPPLY_VOLTAGE = 5;

    /**
     * @internal
     */
    const FUNCTION_SET_CLOCK_FREQUENCY = 7;

    /**
     * @internal
     */
    const FUNCTION_GET_CLOCK_FREQUENCY = 8;

    /**
     * @internal
     */
    const FUNCTION_GET_IDENTITY = 255;


    const DEVICE_IDENTIFIER = 231;

    /**
     * Creates an object with the unique device ID $uid. This object can
     * then be added to the IP connection.
     *
     * @param string $uid
     */
    public function __construct($uid, $ipcon)
    {
        parent::__construct($uid, $ipcon);

        $this->apiVersion = array(2, 0, 1);

        $this->responseExpected[self::FUNCTION_SET_RGB_VALUES] = self::RESPONSE_EXPECTED_FALSE;
        $this->responseExpected[self::FUNCTION_GET_RGB_VALUES] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->responseExpected[self::FUNCTION_SET_FRAME_DURATION] = self::RESPONSE_EXPECTED_FALSE;
        $this->responseExpected[self::FUNCTION_GET_FRAME_DURATION] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->responseExpected[self::FUNCTION_GET_SUPPLY_VOLTAGE] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->responseExpected[self::CALLBACK_FRAME_RENDERED] = self::RESPONSE_EXPECTED_ALWAYS_FALSE;
        $this->responseExpected[self::FUNCTION_SET_CLOCK_FREQUENCY] = self::RESPONSE_EXPECTED_FALSE;
        $this->responseExpected[self::FUNCTION_GET_CLOCK_FREQUENCY] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->responseExpected[self::FUNCTION_GET_IDENTITY] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;

        $this->callbackWrappers[self::CALLBACK_FRAME_RENDERED] = 'callbackWrapperFrameRendered';
    }

    /**
     * @internal
     * @param string $header
     * @param string $data
     */
    public function handleCallback($header, $data)
    {
        call_user_func(array($this, $this->callbackWrappers[$header['functionID']]), $data);
    }

    /**
     * Sets the *rgb* values for the LEDs with the given *length* starting
     * from *index*.
     *
     * The maximum length is 16, the index goes from 0 to 319 and the rgb values
     * have 8 bits each.
     *
     * Example: If you set
     *
     * * index to 5,
     * * length to 3,
     * * r to array(255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
     * * g to array(0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) and
     * * b to array(0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
     *
     * the LED with index 5 will be red, 6 will be green and 7 will be blue.
     *
     * The colors will be transfered to actual LEDs when the next
     * frame duration ends, see BrickletLEDStrip::setFrameDuration().
     *
     * Generic approach:
     *
     * * Set the frame duration to a value that represents
     *   the number of frames per second you want to achieve.
     * * Set all of the LED colors for one frame.
     * * Wait for the BrickletLEDStrip::CALLBACK_FRAME_RENDERED callback.
     * * Set all of the LED colors for next frame.
     * * Wait for the BrickletLEDStrip::CALLBACK_FRAME_RENDERED callback.
     * * and so on.
     *
     * This approach ensures that you can change the LED colors with
     * a fixed frame rate.
     *
     * The actual number of controllable LEDs depends on the number of free
     * Bricklet ports. See :ref:`here <led_strip_bricklet_ram_constraints>` for more
     * information. A call of BrickletLEDStrip::setRGBValues() with index + length above the
     * bounds is ignored completely.
     *
     * @param int $index
     * @param int $length
     * @param int[] $r
     * @param int[] $g
     * @param int[] $b
     *
     * @return void
     */
    public function setRGBValues($index, $length, $r, $g, $b)
    {
        $payload = '';
        $payload .= pack('v', $index);
        $payload .= pack('C', $length);
        for ($i = 0; $i < 16; $i++) {
            $payload .= pack('C', $r[$i]);
        }
        for ($i = 0; $i < 16; $i++) {
            $payload .= pack('C', $g[$i]);
        }
        for ($i = 0; $i < 16; $i++) {
            $payload .= pack('C', $b[$i]);
        }

        $this->sendRequest(self::FUNCTION_SET_RGB_VALUES, $payload);
    }

    /**
     * Returns the rgb with the given *length* starting from the
     * given *index*.
     *
     * The values are the last values that were set by BrickletLEDStrip::setRGBValues().
     *
     * @param int $index
     * @param int $length
     *
     * @return array
     */
    public function getRGBValues($index, $length)
    {
        $result = array();

        $payload = '';
        $payload .= pack('v', $index);
        $payload .= pack('C', $length);

        $data = $this->sendRequest(self::FUNCTION_GET_RGB_VALUES, $payload);

        $payload = unpack('C16r/C16g/C16b', $data);

        $result['r'] = IPConnection::collectUnpackedArray($payload, 'r', 16);
        $result['g'] = IPConnection::collectUnpackedArray($payload, 'g', 16);
        $result['b'] = IPConnection::collectUnpackedArray($payload, 'b', 16);

        return $result;
    }

    /**
     * Sets the frame duration in ms.
     *
     * Example: If you want to achieve 20 frames per second, you should
     * set the frame duration to 50ms (50ms * 20 = 1 second).
     *
     * For an explanation of the general approach see BrickletLEDStrip::setRGBValues().
     *
     * Default value: 100ms (10 frames per second).
     *
     * @param int $duration
     *
     * @return void
     */
    public function setFrameDuration($duration)
    {
        $payload = '';
        $payload .= pack('v', $duration);

        $this->sendRequest(self::FUNCTION_SET_FRAME_DURATION, $payload);
    }

    /**
     * Returns the frame duration as set by BrickletLEDStrip::setFrameDuration().
     *
     *
     * @return int
     */
    public function getFrameDuration()
    {
        $payload = '';

        $data = $this->sendRequest(self::FUNCTION_GET_FRAME_DURATION, $payload);

        $payload = unpack('v1duration', $data);

        return $payload['duration'];
    }

    /**
     * Returns the current supply voltage of the LEDs. The voltage is given in mV.
     *
     *
     * @return int
     */
    public function getSupplyVoltage()
    {
        $payload = '';

        $data = $this->sendRequest(self::FUNCTION_GET_SUPPLY_VOLTAGE, $payload);

        $payload = unpack('v1voltage', $data);

        return $payload['voltage'];
    }

    /**
     * Sets the frequency of the clock in Hz. The range is 10000Hz (10kHz) up to
     * 2000000Hz (2MHz).
     *
     * The Bricklet will choose the nearest achievable frequency, which may
     * be off by a few Hz. You can get the exact frequency that is used by
     * calling BrickletLEDStrip::getClockFrequency().
     *
     * If you have problems with flickering LEDs, they may be bits flipping. You
     * can fix this by either making the connection between the LEDs and the
     * Bricklet shorter or by reducing the frequency.
     *
     * With a decreasing frequency your maximum frames per second will decrease
     * too.
     *
     * The default value is 1.66MHz.
     *
     * <note>
     *  The frequency in firmware version 2.0.0 is fixed at 2MHz.
     * </note>
     *
     * .. versionadded:: 2.0.1~(Plugin)
     *
     * @param int $frequency
     *
     * @return void
     */
    public function setClockFrequency($frequency)
    {
        $payload = '';
        $payload .= pack('V', $frequency);

        $this->sendRequest(self::FUNCTION_SET_CLOCK_FREQUENCY, $payload);
    }

    /**
     * Returns the currently used clock frequency.
     *
     * .. versionadded:: 2.0.1~(Plugin)
     *
     *
     * @return int
     */
    public function getClockFrequency()
    {
        $payload = '';

        $data = $this->sendRequest(self::FUNCTION_GET_CLOCK_FREQUENCY, $payload);

        $payload = unpack('V1frequency', $data);

        return IPConnection::fixUnpackedUInt32($payload['frequency']);
    }

    /**
     * Returns the UID, the UID where the Bricklet is connected to,
     * the position, the hardware and firmware version as well as the
     * device identifier.
     *
     * The position can be 'a', 'b', 'c' or 'd'.
     *
     * The device identifiers can be found :ref:`here <device_identifier>`.
     *
     * .. versionadded:: 2.0.0~(Plugin)
     *
     *
     * @return array
     */
    public function getIdentity()
    {
        $result = array();

        $payload = '';

        $data = $this->sendRequest(self::FUNCTION_GET_IDENTITY, $payload);

        $payload = unpack('c8uid/c8connected_uid/c1position/C3hardware_version/C3firmware_version/v1device_identifier', $data);

        $result['uid'] = IPConnection::implodeUnpackedString($payload, 'uid', 8);
        $result['connected_uid'] = IPConnection::implodeUnpackedString($payload, 'connected_uid', 8);
        $result['position'] = chr($payload['position']);
        $result['hardware_version'] = IPConnection::collectUnpackedArray($payload, 'hardware_version', 3);
        $result['firmware_version'] = IPConnection::collectUnpackedArray($payload, 'firmware_version', 3);
        $result['device_identifier'] = $payload['device_identifier'];

        return $result;
    }

    /**
     * Registers a callback with ID $id to the callable $callback.
     *
     * @param int $id
     * @param callable $callback
     * @param mixed $userData
     *
     * @return void
     */
    public function registerCallback($id, $callback, $userData = NULL)
    {
        $this->registeredCallbacks[$id] = $callback;
        $this->registeredCallbackUserData[$id] = $userData;
    }

    /**
     * @internal
     * @param string $data
     */
    public function callbackWrapperFrameRendered($data)
    {
        $result = array();
        $payload = unpack('v1length', $data);

        array_push($result, $payload['length']);

        call_user_func_array($this->registeredCallbacks[self::CALLBACK_FRAME_RENDERED], $result);
    }
}

?>
