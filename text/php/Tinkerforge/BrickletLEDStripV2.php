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
 * Controls up to 2048 RGB(W) LEDs
 */
class BrickletLEDStripV2 extends Device
{

    /**
     * This callback is triggered directly after a new frame render is started.
     * The parameter is the number of LEDs in that frame.
     * 
     * You should send the data for the next frame directly after this callback
     * was triggered.
     * 
     * For an explanation of the general approach see BrickletLEDStripV2::setLEDValues().
     */
    const CALLBACK_FRAME_STARTED = 6;


    /**
     * @internal
     */
    const FUNCTION_SET_LED_VALUES_LOW_LEVEL = 1;

    /**
     * @internal
     */
    const FUNCTION_GET_LED_VALUES_LOW_LEVEL = 2;

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
    const FUNCTION_SET_CHANNEL_MAPPING = 11;

    /**
     * @internal
     */
    const FUNCTION_GET_CHANNEL_MAPPING = 12;

    /**
     * @internal
     */
    const FUNCTION_SET_FRAME_STARTED_CALLBACK_CONFIGURATION = 13;

    /**
     * @internal
     */
    const FUNCTION_GET_FRAME_STARTED_CALLBACK_CONFIGURATION = 14;

    /**
     * @internal
     */
    const FUNCTION_GET_SPITFP_ERROR_COUNT = 234;

    /**
     * @internal
     */
    const FUNCTION_SET_BOOTLOADER_MODE = 235;

    /**
     * @internal
     */
    const FUNCTION_GET_BOOTLOADER_MODE = 236;

    /**
     * @internal
     */
    const FUNCTION_SET_WRITE_FIRMWARE_POINTER = 237;

    /**
     * @internal
     */
    const FUNCTION_WRITE_FIRMWARE = 238;

    /**
     * @internal
     */
    const FUNCTION_SET_STATUS_LED_CONFIG = 239;

    /**
     * @internal
     */
    const FUNCTION_GET_STATUS_LED_CONFIG = 240;

    /**
     * @internal
     */
    const FUNCTION_GET_CHIP_TEMPERATURE = 242;

    /**
     * @internal
     */
    const FUNCTION_RESET = 243;

    /**
     * @internal
     */
    const FUNCTION_WRITE_UID = 248;

    /**
     * @internal
     */
    const FUNCTION_READ_UID = 249;

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
    const BOOTLOADER_MODE_BOOTLOADER = 0;
    const BOOTLOADER_MODE_FIRMWARE = 1;
    const BOOTLOADER_MODE_BOOTLOADER_WAIT_FOR_REBOOT = 2;
    const BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_REBOOT = 3;
    const BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_ERASE_AND_REBOOT = 4;
    const BOOTLOADER_STATUS_OK = 0;
    const BOOTLOADER_STATUS_INVALID_MODE = 1;
    const BOOTLOADER_STATUS_NO_CHANGE = 2;
    const BOOTLOADER_STATUS_ENTRY_FUNCTION_NOT_PRESENT = 3;
    const BOOTLOADER_STATUS_DEVICE_IDENTIFIER_INCORRECT = 4;
    const BOOTLOADER_STATUS_CRC_MISMATCH = 5;
    const STATUS_LED_CONFIG_OFF = 0;
    const STATUS_LED_CONFIG_ON = 1;
    const STATUS_LED_CONFIG_SHOW_HEARTBEAT = 2;
    const STATUS_LED_CONFIG_SHOW_STATUS = 3;

    const DEVICE_IDENTIFIER = 2103;

    const DEVICE_DISPLAY_NAME = "LED Strip Bricklet 2.0";

    /**
     * Creates an object with the unique device ID $uid. This object can
     * then be added to the IP connection.
     *
     * @param string $uid
     */
    public function __construct($uid, $ipcon)
    {
        parent::__construct($uid, $ipcon);

        $this->api_version = array(2, 0, 0);

        $this->response_expected[self::FUNCTION_SET_LED_VALUES_LOW_LEVEL] = self::RESPONSE_EXPECTED_TRUE;
        $this->response_expected[self::FUNCTION_GET_LED_VALUES_LOW_LEVEL] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_SET_FRAME_DURATION] = self::RESPONSE_EXPECTED_FALSE;
        $this->response_expected[self::FUNCTION_GET_FRAME_DURATION] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_GET_SUPPLY_VOLTAGE] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_SET_CLOCK_FREQUENCY] = self::RESPONSE_EXPECTED_FALSE;
        $this->response_expected[self::FUNCTION_GET_CLOCK_FREQUENCY] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_SET_CHIP_TYPE] = self::RESPONSE_EXPECTED_FALSE;
        $this->response_expected[self::FUNCTION_GET_CHIP_TYPE] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_SET_CHANNEL_MAPPING] = self::RESPONSE_EXPECTED_FALSE;
        $this->response_expected[self::FUNCTION_GET_CHANNEL_MAPPING] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_SET_FRAME_STARTED_CALLBACK_CONFIGURATION] = self::RESPONSE_EXPECTED_TRUE;
        $this->response_expected[self::FUNCTION_GET_FRAME_STARTED_CALLBACK_CONFIGURATION] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_GET_SPITFP_ERROR_COUNT] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_SET_BOOTLOADER_MODE] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_GET_BOOTLOADER_MODE] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_SET_WRITE_FIRMWARE_POINTER] = self::RESPONSE_EXPECTED_FALSE;
        $this->response_expected[self::FUNCTION_WRITE_FIRMWARE] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_SET_STATUS_LED_CONFIG] = self::RESPONSE_EXPECTED_FALSE;
        $this->response_expected[self::FUNCTION_GET_STATUS_LED_CONFIG] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_GET_CHIP_TEMPERATURE] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_RESET] = self::RESPONSE_EXPECTED_FALSE;
        $this->response_expected[self::FUNCTION_WRITE_UID] = self::RESPONSE_EXPECTED_FALSE;
        $this->response_expected[self::FUNCTION_READ_UID] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_GET_IDENTITY] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;

        $this->callback_wrappers[self::CALLBACK_FRAME_STARTED] = 'callbackWrapperFrameStarted';
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
     * Sets the RGB(W) values for the LEDs starting from *index*.
     * You can set at most 2048 RGB values or 1536 RGBW values.
     * 
     * To make the colors show correctly you need to configure the chip type
     * (see BrickletLEDStripV2::setChipType()) and a channel mapping (see BrickletLEDStripV2::setChannelMapping())
     * according to the connected LEDs.
     * 
     * If the channel mapping has 3 colors, you need to give the data in the sequence
     * RGBRGBRGB... if the channel mapping has 4 colors you need to give data in the
     * sequence RGBWRGBWRGBW...
     * 
     * The data is double buffered and the colors will be transfered to the
     * LEDs when the next frame duration ends (see BrickletLEDStripV2::setFrameDuration()).
     * 
     * Generic approach:
     * 
     * * Set the frame duration to a value that represents the number of frames per
     *   second you want to achieve.
     * * Set all of the LED colors for one frame.
     * * Wait for the BrickletLEDStripV2::CALLBACK_FRAME_STARTED callback.
     * * Set all of the LED colors for next frame.
     * * Wait for the BrickletLEDStripV2::CALLBACK_FRAME_STARTED callback.
     * * And so on.
     * 
     * This approach ensures that you can change the LED colors with a fixed frame rate.
     * 
     * @param int $index
     * @param int $value_length
     * @param int $value_chunk_offset
     * @param int[] $value_chunk_data
     * 
     * @return void
     */
    public function setLEDValuesLowLevel($index, $value_length, $value_chunk_offset, $value_chunk_data)
    {
        $payload = '';
        $payload .= pack('v', $index);
        $payload .= pack('v', $value_length);
        $payload .= pack('v', $value_chunk_offset);
        for ($i = 0; $i < 58; $i++) {
            $payload .= pack('C', $value_chunk_data[$i]);
        }

        $this->sendRequest(self::FUNCTION_SET_LED_VALUES_LOW_LEVEL, $payload);
    }

    /**
     * Returns the RGB(W) values as set by BrickletLEDStripV2::setLEDValues().
     * 
     * @param int $index
     * @param int $length
     * 
     * @return array
     */
    public function getLEDValuesLowLevel($index, $length)
    {
        $ret = array();

        $payload = '';
        $payload .= pack('v', $index);
        $payload .= pack('v', $length);

        $data = $this->sendRequest(self::FUNCTION_GET_LED_VALUES_LOW_LEVEL, $payload);

        $payload = unpack('v1value_length/v1value_chunk_offset/C60value_chunk_data', $data);

        $ret['value_length'] = $payload['value_length'];
        $ret['value_chunk_offset'] = $payload['value_chunk_offset'];
        $ret['value_chunk_data'] = IPConnection::collectUnpackedArray($payload, 'value_chunk_data', 60);

        return $ret;
    }

    /**
     * Sets the frame duration in ms.
     * 
     * Example: If you want to achieve 20 frames per second, you should
     * set the frame duration to 50ms (50ms * 20 = 1 second).
     * 
     * For an explanation of the general approach see BrickletLEDStripV2::setLEDValues().
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
     * Returns the frame duration in ms as set by BrickletLEDStripV2::setFrameDuration().
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
     * calling BrickletLEDStripV2::getClockFrequency().
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
     * Returns the currently used clock frequency as set by BrickletLEDStripV2::setClockFrequency().
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
     * Returns the currently used chip type as set by BrickletLEDStripV2::setChipType().
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
     * Sets the channel mapping for the connected LEDs.
     * 
     * If the mapping has 4 colors, the function BrickletLEDStripV2::setLEDValues() expects 4
     * values per pixel and if the mapping has 3 colors it expects 3 values per pixel.
     * 
     * The function always expects the order RGB(W). The connected LED driver chips 
     * might have their 3 or 4 channels in a different order. For example, the WS2801 
     * chips typically use BGR order, then WS2812 chips typically use GRB order and 
     * the APA102 chips typically use WBGR order.
     * 
     * The APA102 chips are special. They have three 8-bit channels for RGB
     * and an additional 5-bit channel for the overall brightness of the RGB LED
     * making them 4-channel chips. Internally the brightness channel is the first
     * channel, therefore one of the Wxyz channel mappings should be used. Then
     * the W channel controls the brightness.
     * 
     * The default value is BGR (36).
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
     * Returns the currently used channel mapping as set by BrickletLEDStripV2::setChannelMapping().
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
     * Enables/disables the BrickletLEDStripV2::CALLBACK_FRAME_STARTED callback.
     * 
     * By default the callback is enabled.
     * 
     * @param bool $enable
     * 
     * @return void
     */
    public function setFrameStartedCallbackConfiguration($enable)
    {
        $payload = '';
        $payload .= pack('C', intval((bool)$enable));

        $this->sendRequest(self::FUNCTION_SET_FRAME_STARTED_CALLBACK_CONFIGURATION, $payload);
    }

    /**
     * Returns the configuration as set by
     * BrickletLEDStripV2::setFrameStartedCallbackConfiguration().
     * 
     * 
     * @return bool
     */
    public function getFrameStartedCallbackConfiguration()
    {
        $payload = '';

        $data = $this->sendRequest(self::FUNCTION_GET_FRAME_STARTED_CALLBACK_CONFIGURATION, $payload);

        $payload = unpack('C1enable', $data);

        return (bool)$payload['enable'];
    }

    /**
     * Returns the error count for the communication between Brick and Bricklet.
     * 
     * The errors are divided into
     * 
     * * ack checksum errors,
     * * message checksum errors,
     * * frameing errors and
     * * overflow errors.
     * 
     * The errors counts are for errors that occur on the Bricklet side. All
     * Bricks have a similar function that returns the errors on the Brick side.
     * 
     * 
     * @return array
     */
    public function getSPITFPErrorCount()
    {
        $ret = array();

        $payload = '';

        $data = $this->sendRequest(self::FUNCTION_GET_SPITFP_ERROR_COUNT, $payload);

        $payload = unpack('V1error_count_ack_checksum/V1error_count_message_checksum/V1error_count_frame/V1error_count_overflow', $data);

        $ret['error_count_ack_checksum'] = IPConnection::fixUnpackedUInt32($payload, 'error_count_ack_checksum');
        $ret['error_count_message_checksum'] = IPConnection::fixUnpackedUInt32($payload, 'error_count_message_checksum');
        $ret['error_count_frame'] = IPConnection::fixUnpackedUInt32($payload, 'error_count_frame');
        $ret['error_count_overflow'] = IPConnection::fixUnpackedUInt32($payload, 'error_count_overflow');

        return $ret;
    }

    /**
     * Sets the bootloader mode and returns the status after the requested
     * mode change was instigated.
     * 
     * You can change from bootloader mode to firmware mode and vice versa. A change
     * from bootloader mode to firmware mode will only take place if the entry function,
     * device identifier und crc are present and correct.
     * 
     * This function is used by Brick Viewer during flashing. It should not be
     * necessary to call it in a normal user program.
     * 
     * @param int $mode
     * 
     * @return int
     */
    public function setBootloaderMode($mode)
    {
        $payload = '';
        $payload .= pack('C', $mode);

        $data = $this->sendRequest(self::FUNCTION_SET_BOOTLOADER_MODE, $payload);

        $payload = unpack('C1status', $data);

        return $payload['status'];
    }

    /**
     * Returns the current bootloader mode, see BrickletLEDStripV2::setBootloaderMode().
     * 
     * 
     * @return int
     */
    public function getBootloaderMode()
    {
        $payload = '';

        $data = $this->sendRequest(self::FUNCTION_GET_BOOTLOADER_MODE, $payload);

        $payload = unpack('C1mode', $data);

        return $payload['mode'];
    }

    /**
     * Sets the firmware pointer for BrickletLEDStripV2::writeFirmware(). The pointer has
     * to be increased by chunks of size 64. The data is written to flash
     * every 4 chunks (which equals to one page of size 256).
     * 
     * This function is used by Brick Viewer during flashing. It should not be
     * necessary to call it in a normal user program.
     * 
     * @param int $pointer
     * 
     * @return void
     */
    public function setWriteFirmwarePointer($pointer)
    {
        $payload = '';
        $payload .= pack('V', $pointer);

        $this->sendRequest(self::FUNCTION_SET_WRITE_FIRMWARE_POINTER, $payload);
    }

    /**
     * Writes 64 Bytes of firmware at the position as written by
     * BrickletLEDStripV2::setWriteFirmwarePointer() before. The firmware is written
     * to flash every 4 chunks.
     * 
     * You can only write firmware in bootloader mode.
     * 
     * This function is used by Brick Viewer during flashing. It should not be
     * necessary to call it in a normal user program.
     * 
     * @param int[] $data
     * 
     * @return int
     */
    public function writeFirmware($data)
    {
        $payload = '';
        for ($i = 0; $i < 64; $i++) {
            $payload .= pack('C', $data[$i]);
        }

        $data = $this->sendRequest(self::FUNCTION_WRITE_FIRMWARE, $payload);

        $payload = unpack('C1status', $data);

        return $payload['status'];
    }

    /**
     * Sets the status LED configuration. By default the LED shows
     * communication traffic between Brick and Bricklet, it flickers once
     * for every 10 received data packets.
     * 
     * You can also turn the LED permanently on/off or show a heartbeat.
     * 
     * If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
     * 
     * @param int $config
     * 
     * @return void
     */
    public function setStatusLEDConfig($config)
    {
        $payload = '';
        $payload .= pack('C', $config);

        $this->sendRequest(self::FUNCTION_SET_STATUS_LED_CONFIG, $payload);
    }

    /**
     * Returns the configuration as set by BrickletLEDStripV2::setStatusLEDConfig()
     * 
     * 
     * @return int
     */
    public function getStatusLEDConfig()
    {
        $payload = '';

        $data = $this->sendRequest(self::FUNCTION_GET_STATUS_LED_CONFIG, $payload);

        $payload = unpack('C1config', $data);

        return $payload['config'];
    }

    /**
     * Returns the temperature in °C as measured inside the microcontroller. The
     * value returned is not the ambient temperature!
     * 
     * The temperature is only proportional to the real temperature and it has bad
     * accuracy. Practically it is only useful as an indicator for
     * temperature changes.
     * 
     * 
     * @return int
     */
    public function getChipTemperature()
    {
        $payload = '';

        $data = $this->sendRequest(self::FUNCTION_GET_CHIP_TEMPERATURE, $payload);

        $payload = unpack('v1temperature', $data);

        return IPConnection::fixUnpackedInt16($payload, 'temperature');
    }

    /**
     * Calling this function will reset the Bricklet. All configurations
     * will be lost.
     * 
     * After a reset you have to create new device objects,
     * calling functions on the existing ones will result in
     * undefined behavior!
     * 
     * 
     * @return void
     */
    public function reset()
    {
        $payload = '';

        $this->sendRequest(self::FUNCTION_RESET, $payload);
    }

    /**
     * Writes a new UID into flash. If you want to set a new UID
     * you have to decode the Base58 encoded UID string into an
     * integer first.
     * 
     * We recommend that you use Brick Viewer to change the UID.
     * 
     * @param int $uid
     * 
     * @return void
     */
    public function writeUID($uid)
    {
        $payload = '';
        $payload .= pack('V', $uid);

        $this->sendRequest(self::FUNCTION_WRITE_UID, $payload);
    }

    /**
     * Returns the current UID as an integer. Encode as
     * Base58 to get the usual string version.
     * 
     * 
     * @return int
     */
    public function readUID()
    {
        $payload = '';

        $data = $this->sendRequest(self::FUNCTION_READ_UID, $payload);

        $payload = unpack('V1uid', $data);

        return IPConnection::fixUnpackedUInt32($payload, 'uid');
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
     * Sets the RGB(W) values for the LEDs starting from *index*.
     * You can set at most 2048 RGB values or 1536 RGBW values.
     * 
     * To make the colors show correctly you need to configure the chip type
     * (see BrickletLEDStripV2::setChipType()) and a channel mapping (see BrickletLEDStripV2::setChannelMapping())
     * according to the connected LEDs.
     * 
     * If the channel mapping has 3 colors, you need to give the data in the sequence
     * RGBRGBRGB... if the channel mapping has 4 colors you need to give data in the
     * sequence RGBWRGBWRGBW...
     * 
     * The data is double buffered and the colors will be transfered to the
     * LEDs when the next frame duration ends (see BrickletLEDStripV2::setFrameDuration()).
     * 
     * Generic approach:
     * 
     * * Set the frame duration to a value that represents the number of frames per
     *   second you want to achieve.
     * * Set all of the LED colors for one frame.
     * * Wait for the BrickletLEDStripV2::CALLBACK_FRAME_STARTED callback.
     * * Set all of the LED colors for next frame.
     * * Wait for the BrickletLEDStripV2::CALLBACK_FRAME_STARTED callback.
     * * And so on.
     * 
     * This approach ensures that you can change the LED colors with a fixed frame rate.
     * 
     * @param int $index
     * @param int[] $value
     * 
     * @return void
     */
    public function setLEDValues($index, $value)
    {
        if (count($value) > 65535) {
            throw new \InvalidArgumentException('Value can be at most 65535 items long');
        }

        $value_length = count($value);
        $value_chunk_offset = 0;

        if ($value_length === 0) {
            $value_chunk_data = array_fill(0, 58);
            $ret = $this->setLEDValuesLowLevel($index, $value_length, $value_chunk_offset, $value_chunk_data);
        } else {
            while ($value_chunk_offset < $value_length) {
                $value_chunk_data = $this->createChunkData($value, $value_chunk_offset, 58, 0);
                $ret = $this->setLEDValuesLowLevel($index, $value_length, $value_chunk_offset, $value_chunk_data);
                $value_chunk_offset += 58;
            }
        }

        return $ret;
    }

    /**
     * Returns the RGB(W) values as set by BrickletLEDStripV2::setLEDValues().
     * 
     * @param int $index
     * @param int $length
     * 
     * @return array
     */
    public function getLEDValues($index, $length)
    {
        $ret = $this->getLEDValuesLowLevel($index, $length);
        $value_length = $ret['value_length'];
        $value_out_of_sync = $ret['value_chunk_offset'] != 0;
        $value_data = $ret['value_chunk_data'];

        while (!$value_out_of_sync && count($value_data) < $value_length) {
            $ret = $this->getLEDValuesLowLevel($index, $length);
            $value_length = $ret['value_length'];
            $value_out_of_sync = $ret['value_chunk_offset'] != count($value_data);
            $value_data = array_merge($value_data, $ret['value_chunk_data']);
        }

        if ($value_out_of_sync) { // discard remaining stream to bring it back in-sync
            while ($ret['value_chunk_offset'] + 60 < $value_length) {
                $ret = $this->getLEDValuesLowLevel($index, $length);
                $value_length = $ret['value_length'];
            }

            throw new StreamOutOfSyncException('Value stream is out-of-sync');
        }

        return array_slice($value_data, 0, $value_length);
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
    public function callbackWrapperFrameStarted($data)
    {
        $payload = unpack('v1length', $data);

        if (array_key_exists(self::CALLBACK_FRAME_STARTED, $this->registered_callbacks)) {
            $function = $this->registered_callbacks[self::CALLBACK_FRAME_STARTED];
            $user_data = $this->registered_callback_user_data[self::CALLBACK_FRAME_STARTED];

            call_user_func($function, $payload['length'], $user_data);
        }
    }
}

?>
