"""Module to control a Sharp Aquos Remote Control enabled TV."""
import socket
import time


class TV(object):
    """
    Description:
        Class representing a Sharp Aquos TV
        Based on documentation from:
            http://files.sharpusa.com/Downloads/ForHome/HomeEntertainment/LCDTVs/Manuals/2014_TV_OM.pdf

    Author: Jeffrey Moore <jmoore987@yahoo.com>

    URL: http://github.com/jmoore/sharp_aquos_rc
    """

    def __init__(self, ip, port, username, password,  # pylint: disable=R0913
                 timeout=5, connection_timeout=2):
        self.ip_address = ip
        self.port = port
        self.auth = str.encode(username + '\r' + password + '\r')
        self.timeout = timeout
        self.connection_timeout = connection_timeout
        if self.timeout <= self.connection_timeout:
            raise ValueError("timeout should be greater than connection_timeout")

    def _send_command(self, code1, code2):
        """
        Description:

            The TV doesn't handle long running connections very well,
            so we open a new connection every time.
            There might be a better way to do this,
            but it's pretty quick and resilient.

        Returns:
            If a value is being requested ( opt2 is "?" ),
            then the return value is returned.
            If a value is being set,
            it returns True for "OK" or False for "ERR"
        """
        # According to the documentation:
        # http://files.sharpusa.com/Downloads/ForHome/
        # HomeEntertainment/LCDTVs/Manuals/tel_man_LC40_46_52_60LE830U.pdf
        # Page 58 - Communication conditions for IP
        # The connection could be lost (but not only after 3 minutes),
        # so we need to the remote commands to be sure about states
        end_time = time.time() + self.timeout
        while time.time() < end_time:
            try:
                # Connect
                sock_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock_con.settimeout(self.connection_timeout)
                sock_con.connect((self.ip_address, self.port))

                # Authenticate
                sock_con.send(self.auth)
                sock_con.recv(1024)
                sock_con.recv(1024)

                # Send command
                sock_con.send(str.encode(code1 + str(code2).ljust(4) + '\r'))
                status = bytes.decode(sock_con.recv(1024)).strip()
            except (OSError, socket.error) as exp:
                time.sleep(0.1)
                if time.time() >= end_time:
                    raise exp
            else:
                sock_con.close()
                # Sometimes the status is empty so
                # We need to retry
                if status != u'':
                    break

        if status == "OK":
            return True
        elif status == "ERR":
            return False
        else:
            try:
                return int(status)
            except ValueError:
                return status

    def info(self):
        """
        Description:

            Returns dict of information about the TV
            name, model, version

        """
        return {"name": self._send_command('TVNM', '1'),
                "model": self._send_command('MNRD', '1'),
                "version": self._send_command('SWVN', '1')
               }

    def power_on_command_settings(self, opt='?'):
        """
        Description:

            Manage whether or not the TV will respond to power() on/off commands
            Call with no arguments to get current setting

        Arguments:
            opt: integer
                0: disabled
                1: accepted via RS232
                2: accepted via TCP/IP
        """
        return self._send_command('RSPW', opt)

    def power(self, opt='?'):
        """
        Description:

            Power On/Off
            Call with no arguments to get current setting

        Arguments:
            opt: integer
                0: Off
                1: On
        """
        return self._send_command('POWR', opt)

    def input(self, opt='?'):
        """
        Description:

            Set the input
            Call with no arguments to get current setting

        Arguments:
            opt: integer
                0: TV / Antenna
                1: HDMI_IN_1
                2: HDMI_IN_2
                3: HDMI_IN_3
                4: HDMI_IN_4
                5: COMPONENT IN
                6: VIDEO_IN_1
                7: VIDEO_IN_2
                8: PC_IN
        """

        if opt == 0:
            return self._send_command('ITVD', opt)
        else:
            return self._send_command('IAVD', opt)

    def av_mode(self, opt='?'):
        """
        Description:

            Set the A/V Mode
            Call with no arguments to get current setting

        Arguments:
            opt: integer
                0: Toggle
                1: Standard (ENERGYSTAR)
                2: Movie
                3: Game
                4: User
                5: Dynamic (Fixed)
                6: Dynamic
                7: PC
                8: x.v. Color
                13: Vintage Movie
                14: Standard 3D
                15: Movie 3D
                16: Game 3D
                17: Movie THX
                100: Auto
        """
        return self._send_command('AVMD', opt)

    def volume(self, opt='?'):
        """
        Description:

            Set the Volume
            Call with no arguments to get current setting

        Arguments:
            opt: integer
            0 - 100: Volume Level
        """
        return self._send_command('VOLM', opt)

    def view_mode(self, opt='?'):
        """
        Description:

            Set the View Mode
            Call with no arguments to get current setting

        Arguments:
            opt: integer
                0: Toggle [AV]
                1: Side Bar [AV]
                2: S. Stretch [AV]
                3: Zoom [AV]
                4: Stretch [AV]
                5: Normal [PC]
                6: Zoom [PC]
                7: Stretch [PC]
                8: Dot by Dot [PC]
                9: Full Screen [AV]
                10: Auto
                11: Original
        """
        return self._send_command('WIDE', opt)

    def mute(self, opt='?'):
        """
        Description:

            Mute On/Off
            Call with no arguments to get current setting

        Arguments:
            opt: integer
                0: Toggle
                1: On
                2: Off
        """
        return self._send_command('MUTE', opt)

    def surround(self, opt='?'):
        """
        Description:

            Set Surround Sound mode
            Call with no arguments to get current setting

        Arguments:
            opt: integer
                0: Toggle
                1: On / Normal
                2: Off
                4: 3D Hall
                5: 3D Movie
                6: 3D Standard
                7: 3D Stadium
        """
        return self._send_command('ACSU', opt)

    def sleep(self, opt='?'):
        """
        Description:

            Set Sleep Timer
            Call with no arguments to get minutes until poweroff

        Arguments:
            opt: integer
                0: Off
                1: 30 minutes
                2: 60 minutes
                3: 90 minutes
                4: 120 minutes
        """
        return self._send_command('OFTM', opt)

    def analog_channel(self, opt='?'):
        """
        Description:

            Change Channel (Analog)
            Call with no arguments to get current setting

        Arguments:
            opt: integer
                (1-135): Channel
        """
        return self._send_command('DCCH', opt)

    def digital_channel_air(self, opt1='?', opt2=1):
        """
        Description:

            Change Channel (Digital)
            Pass Channels "XX.YY" as TV.digital_channel_air(XX, YY)

        Arguments:
            opt1: integer
                1-99: Major Channel
            opt2: integer (optional)
                1-99: Minor Channel
        """
        if opt1 == '?':
            return self._send_command('DA2P', opt1)
        return self._send_command('DA2P', (opt1 * 100) + opt2)

    def digital_channel_cable(self, opt1='?', opt2=1):
        """
        Description:

            Change Channel (Digital)
            Pass Channels "XXX.YYY" as TV.digital_channel_cable(XXX, YYY)

        Arguments:
            opt1: integer
                1-999: Major Channel
            opt2: integer (optional)
                0-999: Minor Channel
        """
        if opt1 == '?':
            return self._send_command('DC2U', '?')
        self._send_command('DC2U', str(opt1).rjust(3, "0"))
        return self._send_command('DC2L', str(opt2).rjust(3, "0"))

    def channel_up(self):
        """
        Description:
            Change the Channel +1
        """
        self._send_command('CHUP', 1)

    def channel_down(self):
        """
        Description:
            Change the Channel -1
        """
        self._send_command('CHDW', 1)

    def remote_button(self, opt='?'):
        """
        Description:

            Press a remote control button

        Arguments:
            opt: integer
                0-9: 0-9
                10: DOT
                11: ENT
                12: POWER
                13: DISPLAY
                14: POWER (SOURCE)
                15: REWIND
                16: PLAY
                17: FAST FORWARD
                18: PAUSE
                19: SKIP BACK
                20: STOP
                21: SKIP FORWARD
                23: OPTION
                24: SLEEP
                27: CC
                28: AV MODE
                29: VIEW MODE
                30: FLASHBACK
                31: MUTE
                32: VOL -
                33: VOL +
                34: CH UP
                35: CH DOWN
                36: INPUT
                38: MENU
                39: SmartCentral
                40: ENTER
                41: UP
                42: DOWN
                43: LEFT
                44: RIGHT
                45: RETURN
                46: EXIT
                47: FAVORITE CH
                49: AUDIO
                50: A (red)
                51: B (green)
                52: C (blue)
                53: D (yellow)
                54: FREEZE
                55: FAV APP 1
                56: FAV APP 2
                57: FAV APP 3
                58: 2D/3D
                59: NETFLIX
                60: AAL
                61: MANUAL
        """
        return self._send_command('RCKY', opt)
