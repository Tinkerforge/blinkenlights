<?php

/* ***********************************************************
 * This file was automatically generated on 2018-06-07.      *
 *                                                           *
 * PHP Bindings Version 2.1.16                               *
 *                                                           *
 * If you have a bugfix for this file and want to commit it, *
 * please fix the bug in the generator. You can find a link  *
 * to the generators git repository on tinkerforge.com       *
 *************************************************************/

namespace Tinkerforge;

require_once(__DIR__ . '/IPConnection.php');

/**
 * Controls up to 320 RGB LEDs
 */
class BrickletLEDStrip extends Device
{

    /**
     * This callback is triggered directly after a new frame is rendered. The
     * parameter is the number of LEDs in that frame.
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
    const FUNCTION_SET_CHIP_TYPE = 9;

    /**
     * @internal
     */
    const FUNCTION_GET_CHIP_TYPE = 10;

    /**
     * @internal
     */
    const FUNCTION_SET_RGBW_VALUES = 11;

    /**
     * @internal
     */
    const FUNCTION_GET_RGBW_VALUES = 12;

    /**
     * @internal
     */
    const FUNCTION_SET_CHANNEL_MAPPING = 13;

    /**
     * @internal
     */
    const FUNCTION_GET_CHANNEL_MAPPING = 14;

    /**
     * @internal
     */
    const FUNCTION_ENABLE_FRAME_RENDERED_CALLBACK = 15;

    /**
     * @internal
     */
    const FUNCTION_DISABLE_FRAME_RENDERED_CALLBACK = 16;

    /**
     * @internal
     */
    const FUNCTION_IS_FRAME_RENDERED_CALLBACK_ENABLED = 17;

    /**
     * @internal
     */
    const FUNCTION_GET_IDENTITY = 255;

    const CHIP_TYPE_WS2801 = 2801;
    const CHIP_TYPE_WS2811 = 2811;
    const CHIP_TYPE_WS2812 = 2812;
    const CHIP_TYPE_LPD8806 = 8806;
    const CHIP_TYPE_APA102 = 102;
    const CHANNEL_MAPPING_RGB = 6;
    const CHANNEL_MAPPING_RBG = 9;
    const CHANNEL_MAPPING_BRG = 33;
    const CHANNEL_MAPPING_BGR = 36;
    const CHANNEL_MAPPING_GRB = 18;
    const CHANNEL_MAPPING_GBR = 24;
    const CHANNEL_MAPPING_RGBW = 27;
    const CHANNEL_MAPPING_RGWB = 30;
    const CHANNEL_MAPPING_RBGW = 39;
    const CHANNEL_MAPPING_RBWG = 45;
    const CHANNEL_MAPPING_RWGB = 54;
    const CHANNEL_MAPPING_RWBG = 57;
    const CHANNEL_MAPPING_GRWB = 78;
    const CHANNEL_MAPPING_GRBW = 75;
    const CHANNEL_MAPPING_GBWR = 108;
    const CHANNEL_MAPPING_GBRW = 99;
    const CHANNEL_MAPPING_GWBR = 120;
    const CHANNEL_MAPPING_GWRB = 114;
    const CHANNEL_MAPPING_BRGW = 135;
    const CHANNEL_MAPPING_BRWG = 141;
    const CHANNEL_MAPPING_BGRW = 147;
    const CHANNEL_MAPPING_BGWR = 156;
    const CHANNEL_MAPPING_BWRG = 177;
    const CHANNEL_MAPPING_BWGR = 180;
    const CHANNEL_MAPPING_WRBG = 201;
    const CHANNEL_MAPPING_WRGB = 198;
    const CHANNEL_MAPPING_WGBR = 216;
    const CHANNEL_MAPPING_WGRB = 210;
    const CHANNEL_MAPPING_WBGR = 228;
    const CHANNEL_MAPPING_WBRG = 225;

    const DEVICE_IDENTIFIER = 231;

    const DEVICE_DISPLAY_NAME = "LED Strip Bricklet";

    /**
     * Creates an object with the unique device ID $uid. This object can
     * then be added to the IP connection.
     *
     * @param string $uid
     */
    public function __construct($uid, $ipcon)
    {
        parent::__construct($uid, $ipcon);

        $this->api_version = array(2, 0, 3);

        $this->response_expected[self::FUNCTION_SET_RGB_VALUES] = self::RESPONSE_EXPECTED_FALSE;
        $this->response_expected[self::FUNCTION_GET_RGB_VALUES] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_SET_FRAME_DURATION] = self::RESPONSE_EXPECTED_FALSE;
        $this->response_expected[self::FUNCTION_GET_FRAME_DURATION] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_GET_SUPPLY_VOLTAGE] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_SET_CLOCK_FREQUENCY] = self::RESPONSE_EXPECTED_FALSE;
        $this->response_expected[self::FUNCTION_GET_CLOCK_FREQUENCY] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_SET_CHIP_TYPE] = self::RESPONSE_EXPECTED_FALSE;
        $this->response_expected[self::FUNCTION_GET_CHIP_TYPE] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_SET_RGBW_VALUES] = self::RESPONSE_EXPECTED_FALSE;
        $this->response_expected[self::FUNCTION_GET_RGBW_VALUES] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_SET_CHANNEL_MAPPING] = self::RESPONSE_EXPECTED_FALSE;
        $this->response_expected[self::FUNCTION_GET_CHANNEL_MAPPING] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_ENABLE_FRAME_RENDERED_CALLBACK] = self::RESPONSE_EXPECTED_TRUE;
        $this->response_expected[self::FUNCTION_DISABLE_FRAME_RENDERED_CALLBACK] = self::RESPONSE_EXPECTED_TRUE;
        $this->response_expected[self::FUNCTION_IS_FRAME_RENDERED_CALLBACK_ENABLED] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_GET_IDENTITY] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;

        $this->callback_wrappers[self::CALLBACK_FRAME_RENDERED] = 'callbackWrapperFrameRendered';
    }

    /**
     * @internal
     * @param string $header
     * @param string $data
     */
    public function handleCallback($header, $data)
    {
        call_user_func(array($this, $this->callback_wrappers[$header['function_id']]), $data);
    }

    /**
     * Sets the RGB values for the LEDs with the given *length* starting
     * from *index*.
     * 
     * To make the colors show correctly you need to configure the chip type
     * (BrickletLEDStrip::setChipType()) and a 3-channel channel mapping (BrickletLEDStrip::setChannelMapping())
     * according to the connected LEDs.
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
     * \note Depending on the LED circuitry colors can be permuted.
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
     * Returns RGB value with the given *length* starting from the
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
        $ret = array();

        $payload = '';
        $payload .= pack('v', $index);
        $payload .= pack('C', $length);

        $data = $this->sendRequest(self::FUNCTION_GET_RGB_VALUES, $payload);

        $payload = unpack('C16r/C16g/C16b', $data);

        $ret['r'] = IPConnection::collectUnpackedArray($payload, 'r', 16);
        $ret['g'] = IPConnection::collectUnpackedArray($payload, 'g', 16);
        $ret['b'] = IPConnection::collectUnpackedArray($payload, 'b', 16);

        return $ret;
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
     * Returns the frame duration in ms as set by BrickletLEDStrip::setFrameDuration().
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
     * .. versionadded:: 2.0.1$nbsp;(Plugin)
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
     * Returns the currently used clock frequency as set by BrickletLEDStrip::setClockFrequency().
     * 
     * .. versionadded:: 2.0.1$nbsp;(Plugin)
     * 
     * 
     * @return int
     */
    public function getClockFrequency()
    {
        $payload = '';

        $data = $this->sendRequest(self::FUNCTION_GET_CLOCK_FREQUENCY, $payload);

        $payload = unpack('V1frequency', $data);

        return IPConnection::fixUnpackedUInt32($payload, 'frequency');
    }

    /**
     * Sets the type of the LED driver chip. We currently support the chips
     * 
     * * WS2801,
     * * WS2811,
     * * WS2812 / SK6812 / NeoPixel RGB,
     * * SK6812RGBW / NeoPixel RGBW (Chip Type = WS2812),
     * * LPD8806 and
     * * APA102 / DotStar.
     * 
     * The default value is WS2801 (2801).
     * 
     * .. versionadded:: 2.0.2$nbsp;(Plugin)
     * 
     * @param int $chip
     * 
     * @return void
     */
    public function setChipType($chip)
    {
        $payload = '';
        $payload .= pack('v', $chip);

        $this->sendRequest(self::FUNCTION_SET_CHIP_TYPE, $payload);
    }

    /**
     * Returns the currently used chip type as set by BrickletLEDStrip::setChipType().
     * 
     * .. versionadded:: 2.0.2$nbsp;(Plugin)
     * 
     * 
     * @return int
     */
    public function getChipType()
    {
        $payload = '';

        $data = $this->sendRequest(self::FUNCTION_GET_CHIP_TYPE, $payload);

        $payload = unpack('v1chip', $data);

        return $payload['chip'];
    }

    /**
     * Sets the RGBW values for the LEDs with the given *length* starting
     * from *index*.
     * 
     * To make the colors show correctly you need to configure the chip type
     * (BrickletLEDStrip::setChipType()) and a 4-channel channel mapping (BrickletLEDStrip::setChannelMapping())
     * according to the connected LEDs.
     * 
     * The maximum length is 12, the index goes from 0 to 239 and the rgbw values
     * have 8 bits each.
     * 
     * Example: If you set
     * 
     * * index to 5,
     * * length to 4,
     * * r to array(255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
     * * g to array(0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
     * * b to array(0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0) and
     * * w to array(0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0)
     * 
     * the LED with index 5 will be red, 6 will be green, 7 will be blue and 8 will be white.
     * 
     * \note Depending on the LED circuitry colors can be permuted.
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
     * information. A call of BrickletLEDStrip::setRGBWValues() with index + length above the
     * bounds is ignored completely.
     * 
     * The LPD8806 LED driver chips have 7-bit channels for RGB. Internally the LED
     * Strip Bricklets divides the 8-bit values set using this function by 2 to make
     * them 7-bit. Therefore, you can just use the normal value range (0-255) for
     * LPD8806 LEDs.
     * 
     * The brightness channel of the APA102 LED driver chips has 5-bit. Internally the
     * LED Strip Bricklets divides the 8-bit values set using this function by 8 to make
     * them 5-bit. Therefore, you can just use the normal value range (0-255) for
     * the brightness channel of APA102 LEDs.
     * 
     * .. versionadded:: 2.0.6$nbsp;(Plugin)
     * 
     * @param int $index
     * @param int $length
     * @param int[] $r
     * @param int[] $g
     * @param int[] $b
     * @param int[] $w
     * 
     * @return void
     */
    public function setRGBWValues($index, $length, $r, $g, $b, $w)
    {
        $payload = '';
        $payload .= pack('v', $index);
        $payload .= pack('C', $length);
        for ($i = 0; $i < 12; $i++) {
            $payload .= pack('C', $r[$i]);
        }
        for ($i = 0; $i < 12; $i++) {
            $payload .= pack('C', $g[$i]);
        }
        for ($i = 0; $i < 12; $i++) {
            $payload .= pack('C', $b[$i]);
        }
        for ($i = 0; $i < 12; $i++) {
            $payload .= pack('C', $w[$i]);
        }

        $this->sendRequest(self::FUNCTION_SET_RGBW_VALUES, $payload);
    }

    /**
     * Returns RGBW values with the given *length* starting from the
     * given *index*.
     * 
     * The values are the last values that were set by BrickletLEDStrip::setRGBWValues().
     * 
     * .. versionadded:: 2.0.6$nbsp;(Plugin)
     * 
     * @param int $index
     * @param int $length
     * 
     * @return array
     */
    public function getRGBWValues($index, $length)
    {
        $ret = array();

        $payload = '';
        $payload .= pack('v', $index);
        $payload .= pack('C', $length);

        $data = $this->sendRequest(self::FUNCTION_GET_RGBW_VALUES, $payload);

        $payload = unpack('C12r/C12g/C12b/C12w', $data);

        $ret['r'] = IPConnection::collectUnpackedArray($payload, 'r', 12);
        $ret['g'] = IPConnection::collectUnpackedArray($payload, 'g', 12);
        $ret['b'] = IPConnection::collectUnpackedArray($payload, 'b', 12);
        $ret['w'] = IPConnection::collectUnpackedArray($payload, 'w', 12);

        return $ret;
    }

    /**
     * Sets the channel mapping for the connected LEDs.
     * 
     * BrickletLEDStrip::setRGBValues() and BrickletLEDStrip::setRGBWValues() take the data in RGB(W) order.
     * But the connected LED driver chips might have their 3 or 4 channels in a
     * different order. For example, the WS2801 chips typically use BGR order, the
     * WS2812 chips typically use GRB order and the APA102 chips typically use WBGR
     * order.
     * 
     * The APA102 chips are special. They have three 8-bit channels for RGB
     * and an additional 5-bit channel for the overall brightness of the RGB LED
     * making them 4-channel chips. Internally the brightness channel is the first
     * channel, therefore one of the Wxyz channel mappings should be used. Then
     * the W channel controls the brightness.
     * 
     * If a 3-channel mapping is selected then BrickletLEDStrip::setRGBValues() has to be used.
     * Calling BrickletLEDStrip::setRGBWValues() with a 3-channel mapping will produce incorrect
     * results. Vice-versa if a 4-channel mapping is selected then
     * BrickletLEDStrip::setRGBWValues() has to be used. Calling BrickletLEDStrip::setRGBValues() with a
     * 4-channel mapping will produce incorrect results.
     * 
     * The default value is BGR (36).
     * 
     * .. versionadded:: 2.0.6$nbsp;(Plugin)
     * 
     * @param int $mapping
     * 
     * @return void
     */
    public function setChannelMapping($mapping)
    {
        $payload = '';
        $payload .= pack('C', $mapping);

        $this->sendRequest(self::FUNCTION_SET_CHANNEL_MAPPING, $payload);
    }

    /**
     * Returns the currently used channel mapping as set by BrickletLEDStrip::setChannelMapping().
     * 
     * .. versionadded:: 2.0.6$nbsp;(Plugin)
     * 
     * 
     * @return int
     */
    public function getChannelMapping()
    {
        $payload = '';

        $data = $this->sendRequest(self::FUNCTION_GET_CHANNEL_MAPPING, $payload);

        $payload = unpack('C1mapping', $data);

        return $payload['mapping'];
    }

    /**
     * Enables the BrickletLEDStrip::CALLBACK_FRAME_RENDERED callback.
     * 
     * By default the callback is enabled.
     * 
     * .. versionadded:: 2.0.6$nbsp;(Plugin)
     * 
     * 
     * @return void
     */
    public function enableFrameRenderedCallback()
    {
        $payload = '';

        $this->sendRequest(self::FUNCTION_ENABLE_FRAME_RENDERED_CALLBACK, $payload);
    }

    /**
     * Disables the BrickletLEDStrip::CALLBACK_FRAME_RENDERED callback.
     * 
     * By default the callback is enabled.
     * 
     * .. versionadded:: 2.0.6$nbsp;(Plugin)
     * 
     * 
     * @return void
     */
    public function disableFrameRenderedCallback()
    {
        $payload = '';

        $this->sendRequest(self::FUNCTION_DISABLE_FRAME_RENDERED_CALLBACK, $payload);
    }

    /**
     * Returns *true* if the BrickletLEDStrip::CALLBACK_FRAME_RENDERED callback is enabled, *false* otherwise.
     * 
     * .. versionadded:: 2.0.6$nbsp;(Plugin)
     * 
     * 
     * @return bool
     */
    public function isFrameRenderedCallbackEnabled()
    {
        $payload = '';

        $data = $this->sendRequest(self::FUNCTION_IS_FRAME_RENDERED_CALLBACK_ENABLED, $payload);

        $payload = unpack('C1enabled', $data);

        return (bool)$payload['enabled'];
    }

    /**
     * Returns the UID, the UID where the Bricklet is connected to,
     * the position, the hardware and firmware version as well as the
     * device identifier.
     * 
     * The position can be 'a', 'b', 'c' or 'd'.
     * 
     * The device identifier numbers can be found :ref:`here <device_identifier>`.
     * |device_identifier_constant|
     * 
     * 
     * @return array
     */
    public function getIdentity()
    {
        $ret = array();

        $payload = '';

        $data = $this->sendRequest(self::FUNCTION_GET_IDENTITY, $payload);

        $payload = unpack('c8uid/c8connected_uid/c1position/C3hardware_version/C3firmware_version/v1device_identifier', $data);

        $ret['uid'] = IPConnection::implodeUnpackedString($payload, 'uid', 8);
        $ret['connected_uid'] = IPConnection::implodeUnpackedString($payload, 'connected_uid', 8);
        $ret['position'] = chr($payload['position']);
        $ret['hardware_version'] = IPConnection::collectUnpackedArray($payload, 'hardware_version', 3);
        $ret['firmware_version'] = IPConnection::collectUnpackedArray($payload, 'firmware_version', 3);
        $ret['device_identifier'] = $payload['device_identifier'];

        return $ret;
    }

    /**
     * Registers the given $function with the given $callback_id. The optional
     * $user_data will be passed as the last parameter to the $function.
     *
     * @param int $callback_id
     * @param callable $function
     * @param mixed $user_data
     *
     * @return void
     */
    public function registerCallback($callback_id, $function, $user_data = NULL)
    {
        if (!is_callable($function)) {
            throw new \Exception('Function is not callable');
        }

        $this->registered_callbacks[$callback_id] = $function;
        $this->registered_callback_user_data[$callback_id] = $user_data;
    }

    /**
     * @internal
     * @param string $data
     */
    public function callbackWrapperFrameRendered($data)
    {
        $payload = unpack('v1length', $data);

        if (array_key_exists(self::CALLBACK_FRAME_RENDERED, $this->registered_callbacks)) {
            $function = $this->registered_callbacks[self::CALLBACK_FRAME_RENDERED];
            $user_data = $this->registered_callback_user_data[self::CALLBACK_FRAME_RENDERED];

            call_user_func($function, $payload['length'], $user_data);
        }
    }
}

?>
