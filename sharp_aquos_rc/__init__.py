import socket

class TV:
    """
    Description:
        Module to control a Sharp Aquos Remote Control enabled TV.
        Based on documentation from:
            http://files.sharpusa.com/Downloads/ForHome/HomeEntertainment/LCDTVs/Manuals/2014_TV_OM.pdf

    Author: Jeffrey Moore <jmoore987@yahoo.com>

    URL: http://github.com/jmoore/sharp_aquos_rc
    """
    
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.auth = str.encode(username + '\r' + password + '\r')

    def __send__(self, code1, code2):

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip, self.port))
            s.send(self.auth)
            s.recv(1024)
            s.recv(1024)
            s.send(str.encode(code1 + code2.ljust(4) + '\r'))
            status = s.recv(1024)
        except:
            raise
        else:
            s.close()

        return status

    def power_on_command_settings(self, opt = 0):
        """
        Description:
            Change whether or not the TV will respond to power() on/off commands

        Arguments:
            opt: integer
                0: disabled (default)
                1: accepted via RS232
                2: accepted via TCP/IP
        """
        self.__send__('RSPW', opt)

    def power(self, opt = 0):
        """
        Description:
            Power On/Off

        Arguments:
            opt: integer
                0: Off (default)
                1: On
        """
        self.__send__('POWR', opt)

    def input(self, opt = 0):
        """
        Description:
            Set the input

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
            self.__send__('ITVD', opt)
        else:
            self.__send__('IAVD', opt)
        
    def av_mode(self, opt = 0):
        """
        Description:
            Set the A/V Mode

        Arguments:
            opt: integer
                0: Toggle (default)
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
        self.__send__('AVMD', opt)

    def volume(self, opt = 0):
        """
        Description:
            Set the Volume

        Arguments:
            opt: integer
            0 - 100: Volume Level
        """
        self.__send__('VOLM', opt)

    def view_mode(self, opt = 0):
        """
        Description:
            Set the View Mode

        Arguments:
            opt: integer
                0: Toggle (default) [AV]
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
        self.__send__('WIDE', opt)

    def mute(self, opt = 0):
        """
        Description:
            Mute On/Off

        Arguments:
            opt: integer
                0: Toggle (default)
                1: On
                2: Off
        """
        self.__send__('ACSU', opt)

    def surround(self, opt):
        """
        Description:
            Set Surround Sound mode

        Arguments:
            opt: integer
                0: Toggle (default)
                1: On / Normal
                2: Off
                4: 3D Hall
                5: 3D Movie
                6: 3D Standard
                7: 3D Stadium
        """
        self.__send__('ACSU', opt)

    def sleep(self, opt = 0):
        """
        Description:
            Set Sleep Timer

        Arguments:
            opt: integer
                0: Off (default)
                1: 30 minutes
                2: 60 minutes
                3: 90 minutes
                4: 120 minutes
        """
        self.__send__('OFTM', opt)

    def analog_channel(self, opt):
        """
        Description:
            Change Channel (Analog)

        Arguments:
            opt: integer
                (1-135): Channel
        """
        self.__send__('DCCH', opt)

    def digital_channel_air(self, opt1, opt2 = 0):
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
        self.__send__('DA2P', (opt1 * 100) + opt2)

    def digital_channel_cable(self, opt1, opt2 = 0):
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
        self.__send__('DC2U', str(opt1.rjust(3, "0")))
        self.__send__('DC2L', str(opt2.rjust(3, "0")))

    def channel_up():
        """
        Description:
            Change the Channel +1
        """
        self.__send__('CHUP', 1)

    def channel_down():
        """
        Description:
            Change the Channel -1
        """
        self.__send__('CHDW', 1)

        
    
