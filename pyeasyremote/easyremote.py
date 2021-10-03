import socket
from urllib.parse import parse_qs
from colorsys import rgb_to_hsv


class EasyRemote:
    def __init__(self, ip: str, port: int=4003) -> None:
        self.addr = (ip, port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.settimeout(5)
        self.objects = {}

        # Get objects and store them in a name->object dict
        # Because the client screen width and height are required,
        # we just pass 0 and 0. Note that the consequence of this decision is
        # that all the returned x, y positioning info for the objects is
        # useless, because it will all be 0,0 too.
        try:
            self.s.sendto("action=ready&width=0&height=0\r\n".encode(), self.addr)
            recv_objects = True
            while recv_objects:
                msg = self.s.recvfrom(1024)[0].decode()
                action = parse_qs(msg)

                # Add appropriate object for each incoming set_layer action
                if action["action"][0] == "set_layer":
                    self.objects[action["name"][0]] = \
                        EasyRemoteObject.get_easy_remote_object(
                            self, int(action["id"][0]), int(action["page"][0]),
                            action["name"][0], action["type"][0])

                # End the loop when the done action is received
                if action["action"][0] == "done":
                    recv_objects = False
        except socket.timeout:
            self.objects = {}


class EasyRemoteObject:
    """
    This object represents a single control in EasyRemote,
    like a dimmer or a colorwheel. Each type has its own subclass.
    """
    def __init__(self, er: EasyRemote, id: int, page: int, name: str) -> None:
        self.id = id
        self.page = page
        self.name = name
        self.er = er

    @staticmethod
    def get_easy_remote_object(er: EasyRemote, id: int, page: int, name: str,
                               type: str) -> object:
        """
        Returns the appropriate object for the given type. Returns the
        generic EasyRemoteObject if the type is not (yet) supported.
        """
        if type == 'btn':
            return EasyRemoteButton(er, id, page, name)
        elif type == 'sld':
            return EasyRemoteSlider(er, id, page, name)
        elif type == 'pt':
            return EasyRemotePanTilt(er, id, page, name)
        elif type == 'cw':
            return EasyRemoteColorwheel(er, id, page, name)
        else:
            return EasyRemoteObject(er, id, page, name)


class EasyRemoteButton(EasyRemoteObject):
    """
    This object represents a button in EasyRemote.
    """
    def __init__(self, er: EasyRemote, id: int, page: int, name: str) -> None:
        super().__init__(er, id, page, name)

    def set_state(self, state: bool) -> None:
        """
        Sets the button to the given state(True = on).
        """
        # Send EasyRemote update_element event for this button
        # with the given state.
        self.er.s.sendto((f"action=update_element&id={self.id}"
                          f"&page={self.page}&value={int(state)}"
                          "&type=btn&event=up").encode(), self.er.addr)


class EasyRemoteSlider(EasyRemoteObject):
    """
    This object represents a slider in EasyRemote.
    """
    def __init__(self, er: EasyRemote, id: int, page: int, name: str) -> None:
        super().__init__(er, id, page, name)

    def set_value(self, value: int) -> None:
        """
        Sets the slider to the given value.
        Values typically range from 0 to 255.
        """
        # Send EasyRemote update_element event for this slider
        # with the given value.
        self.er.s.sendto((f"action=update_element&id={self.id}"
                          f"&page={self.page}&value={value}"
                          "&type=sld&event=up").encode(), self.er.addr)


class EasyRemotePanTilt(EasyRemoteObject):
    """
    This object represents a pan tilt control object in EasyRemote.
    """
    def __init__(self, er: EasyRemote, id: int, page: int, name: str) -> None:
        super().__init__(er, id, page, name)

    def set_pan_tilt(self, pan: int, tilt: int) -> None:
        """
        Sets the pan and tilt to the given values.
        Values typically range from 0 to 65535.
        """
        # Send EasyRemote update_element event for this pan tilt control
        # with the given pan and tilt values.
        self.er.s.sendto((f"action=update_element&id={self.id}"
                          f"&page={self.page}&value={pan},{tilt}"
                          "&type=pt&event=up").encode(), self.er.addr)


class EasyRemoteColorwheel(EasyRemoteObject):
    """
    This object represents a colorwheel in EasyRemote.
    """
    def __init__(self, er: EasyRemote, id: int, page: int, name: str) -> None:
        super().__init__(er, id, page, name)

    def set_rgb(self, r: int, g: int, b: int) -> None:
        """
        Sets the colorwheel to the given red, green, blue values.
        Values range from 0 to 255.
        """
        self.set_hsv(*rgb_to_hsv(r/255., g/255., b/255.))

    def set_hsv(self, h: float, s: float, v: int) -> None:
        """
        Sets the colorwheel to the given hue, saturation and value.
        Values range from 0 to 1.
        """
        h = round(h * 360)
        s = round(s * 255)
        v = round(v * 255)

        # Send EasyRemote update_element event for this colorwheel
        # with the given hue, saturation and value.
        self.er.s.sendto((f"action=update_element&id={self.id}"
                          f"&page={self.page}&value={h},{s},{v}"
                          "&type=cw&event=up").encode(), self.er.addr)
