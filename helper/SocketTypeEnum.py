from enum import Enum


class SocketTypeEnum(Enum):
    UpdatedCard = 'UpdatedCard'
    WinnerEvent = 'WinnerEvent'
    ErrorMessage = 'ErrorMessage'
    ExtractedNumber = 'ExtractedNumber'
    RoomServiceMessages = 'RoomServiceMessages'
    JoinRoom = 'join_room'
    LeaveRoom = 'leave_room'
