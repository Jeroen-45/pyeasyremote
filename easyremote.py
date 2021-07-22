import socket
from urllib.parse import parse_qs
from colorsys import rgb_to_hsv


class EasyRemote:
    def __init__(self, ip: str, port: int=4003) -> None:
        self.addr = (ip, port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.objects = {}

        # Get objects and store them in a name->object dict
        # Because the client screen width and height are required,
        # we just pass 0 and 0. Note that the consequence of this decision is
        # that all the returned x, y positioning info for the objects is
        # useless, because it will all be 0,0 too.
        self.s.sendto("action=ready&width=0&height=0\r\n".encode(), self.addr)
        recv_objects = True
        while recv_objects:
            msg = self.s.recvfrom(1024)[0].decode()
            print(msg)
            action = parse_qs(msg)

            # Add appropriate object for each incoming set_layer action
            if action["action"][0] == "set_layer":
                self.objects[action["name"][0]] = \
                    EasyRemoteObject.get_easy_remote_object(
                        int(action["id"][0]), int(action["page"][0]),
                        action["name"][0], action["type"][0])

            # End the loop when the done action is received
            if action["action"][0] == "done":
                recv_objects = False


class EasyRemoteObject:
    """
    This object represents a single control in EasyRemote,
    like a dimmer or a colorwheel. Each type has its own subclass.
    """
    def __init__(self, id: int, page: int, name: str) -> None:
        self.id = id
        self.page = page
        self.name = name

    @staticmethod
    def get_easy_remote_object(id: int, page: int, name: str,
                               type: str) -> object:
        """
        Returns the appropriate object for the given type. Returns the
        generic EasyRemoteObject if the type is not (yet) supported.
        """
        if type == 'cw':
            return EasyRemoteColorwheel(id, page, name)
        else:
            return EasyRemoteObject(id, page, name)


class EasyRemoteColorwheel(EasyRemoteObject):
    """
    This object represents a colorwheel in EasyRemote.
    """
    def __init__(self, id: int, page: int, name: str) -> None:
        super().__init__(id, page, name)

    def set_rgb(self, er: EasyRemote, r: int, g: int, b: int) -> None:
        """
        Sets the colorwheel to the given red, green, blue values.
        """
        self.set_hsv(er, *rgb_to_hsv(r/255., g/255., b/255.))

    def set_hsv(self, er: EasyRemote, h: float, s: float, v: int) -> None:
        """
        Sets the colorwheel to the given hue, saturation and value.
        """
        h = round(h * 360)
        s = round(s * 255)
        v = round(v * 255)

        # Send EasyRemote update_element event for the current colorwheel
        # with the given hue, saturation and value.
        er.s.sendto((f"action=update_element&id={self.id}&page={self.page}"
                     f"&value={h},{s},{v}&type=cw&event=up").encode(), er.addr)
