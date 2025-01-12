from typing import cast

from ...schemas.mutations import MutDancerStatusPayload
from ...schemas.queries import (
    QueryColorMapPayload,
    QueryColorMapPayloadItem,
    QueryControlFrame,
    QueryControlMapPayload,
    QueryCoordinatesPayload,
    QueryDancersPayload,
    QueryDancerStatusPayload,
    QueryDancerStatusPayloadItem,
    QueryEffectListControlFrame,
    QueryEffectListItem,
    QueryEffectListPositionFrame,
    QueryLEDMapPayload,
    QueryModelPayload,
    QueryPosFrame,
    QueryPosMapPayload,
    QueryRevision,
)
from ...schemas.subscriptions import (
    SubControlFrame,
    SubEffectListItemData,
    SubLEDRecordDataItem,
    SubPositionFrame,
)
from ..models import (
    Color,
    ColorID,
    ColorMap,
    ControlMap,
    ControlMapElement,
    ControlMapStatus,
    DancerName,
    DancersArray,
    DancersArrayItem,
    DancersArrayPartsItem,
    DancerStatus,
    FiberData,
    LEDBulbData,
    LEDData,
    LEDEffect,
    LEDEffectID,
    LEDMap,
    Location,
    MapID,
    ModelsArray,
    ModelsArrayItem,
    PartData,
    PartName,
    PartType,
    PosMap,
    PosMapElement,
    PosMapStatus,
    Revision,
)
from ..states import state


def models_query_to_state(payload: QueryModelPayload) -> ModelsArray:
    models_array = [
        ModelsArrayItem(name=model.name, dancers=model.dancers) for model in payload
    ]

    return models_array


def dancers_query_to_state(payload: QueryDancersPayload) -> DancersArray:
    dancers_array: DancersArray = []

    for dancer in payload:
        dancerName = dancer.name
        dancerParts = dancer.parts
        dancers_array_item = DancersArrayItem(name=dancerName, parts=[])

        for part in dancerParts:
            dancers_array_item.parts.append(
                DancersArrayPartsItem(
                    name=part.name, type=part.type, length=part.length
                )
            )

        dancers_array.append(dancers_array_item)

    return dancers_array


def pos_frame_query_to_state(payload: QueryPosFrame) -> PosMapElement:
    rev = Revision(meta=payload.rev.meta, data=payload.rev.data)

    pos_map_element = PosMapElement(start=payload.start, pos={}, rev=rev)
    pos_map_element.pos = pos_status_query_to_state(payload.pos)

    return pos_map_element


def pos_frame_sub_to_query(data: SubPositionFrame) -> QueryPosFrame:
    rev = QueryRevision(meta=data.rev.meta, data=data.rev.data)

    response = QueryPosFrame(start=data.start, pos=[], rev=rev)
    response.pos = [(pos[0], pos[1], pos[2]) for pos in data.pos]

    return response


def coordinates_query_to_state(payload: QueryCoordinatesPayload) -> Location:
    return Location(x=payload[0], y=payload[1], z=payload[2])


def pos_status_query_to_state(payload: list[QueryCoordinatesPayload]) -> PosMapStatus:
    pos_map_status: PosMapStatus = {}

    for dancerIndex, dancerStatus in enumerate(payload):
        dancers_array_item = state.dancers_array[dancerIndex]
        dancer_name = dancers_array_item.name

        pos_map_status[dancer_name] = coordinates_query_to_state(dancerStatus)

    return pos_map_status


def pos_map_query_to_state(frames: QueryPosMapPayload) -> PosMap:
    pos_map: PosMap = {}

    for id, frame in frames.items():
        pos_map[id] = pos_frame_query_to_state(frame)

    return pos_map


def part_data_query_to_state(
    part_type: PartType, payload: QueryDancerStatusPayloadItem
) -> PartData:
    match part_type:
        case PartType.LED:
            return LEDData(effect_id=payload[0], alpha=payload[1])
        case PartType.FIBER:
            return FiberData(color_id=payload[0], alpha=payload[1])


def part_data_state_to_mut(
    part_data: PartData,
) -> tuple[LEDEffectID | ColorID, int]:
    if isinstance(part_data, LEDData):
        return (part_data.effect_id, part_data.alpha)
    else:
        return (part_data.color_id, part_data.alpha)


def control_status_query_to_state(
    payload: list[QueryDancerStatusPayload],
) -> ControlMapStatus:
    control_map_status: ControlMapStatus = {}

    for dancerIndex, dancerStatus in enumerate(payload):
        dancers_array_item = state.dancers_array[dancerIndex]
        dancer_name = dancers_array_item.name
        dancer_parts = dancers_array_item.parts
        dancer_status: DancerStatus = {}

        for partIndex, partStatus in enumerate(dancerStatus):
            part_name = dancer_parts[partIndex].name
            part_type = state.part_type_map[part_name]

            dancer_status[part_name] = part_data_query_to_state(part_type, partStatus)

        control_map_status[dancer_name] = dancer_status

    return control_map_status


def control_frame_query_to_state(payload: QueryControlFrame) -> ControlMapElement:
    rev = Revision(meta=payload.rev.meta, data=payload.rev.data)

    control_map_element = ControlMapElement(
        start=payload.start, fade=payload.fade, status={}, rev=rev
    )

    control_map_element.status = control_status_query_to_state(payload.status)

    return control_map_element


def control_map_query_to_state(frames: QueryControlMapPayload) -> ControlMap:
    control_map: ControlMap = {}

    for id, frame in frames.items():
        control_map[id] = control_frame_query_to_state(frame)

    return control_map


def control_frame_sub_to_query(data: SubControlFrame) -> QueryControlFrame:
    rev = QueryRevision(meta=data.rev.meta, data=data.rev.data)

    response = QueryControlFrame(start=data.start, fade=data.fade, status=[], rev=rev)

    response.status = [
        [(partControl[0], partControl[1]) for partControl in partControls]
        for partControls in data.status
    ]

    return response


def control_status_state_to_mut(
    control_status: ControlMapStatus,
) -> list[MutDancerStatusPayload]:
    mut_dancer_status_payload: list[MutDancerStatusPayload] = []

    for dancer in state.dancers_array:
        dancer_name = dancer.name
        dancer_status = control_status.get(dancer_name)
        if dancer_status is None:
            raise Exception("Dancer status not found")

        mut_dancer_status_payload.append(
            [part_data_state_to_mut(dancer_status[part.name]) for part in dancer.parts]
        )

    return mut_dancer_status_payload


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f"#{r:02x}{g:02x}{b:02x}"


def color_query_to_state(id: ColorID, payload: QueryColorMapPayloadItem) -> Color:
    return Color(
        id=id,
        name=payload.color,
        color_code=rgb_to_hex(payload.colorCode),
        rgb=payload.colorCode,
    )


def color_map_query_to_state(payload: QueryColorMapPayload) -> ColorMap:
    color_map: ColorMap = {}

    for id, color in payload.items():
        color_map[id] = Color(
            id=id,
            name=color.color,
            color_code=rgb_to_hex(color.colorCode),
            rgb=color.colorCode,
        )

    return color_map


def led_map_query_to_state(payload: QueryLEDMapPayload) -> LEDMap:
    led_map: LEDMap = {}

    for model_name, parts in payload.items():
        led_map[model_name] = {}
        model_map = led_map[model_name]

        for part_name, effects in parts.items():
            model_map[part_name] = {}
            part_map = model_map[part_name]

            for effect_name, effect in effects.items():
                frame = effect.frames[0]
                bulb_data = [
                    LEDBulbData(color_id=color_id, alpha=alpha)
                    for color_id, alpha in frame.LEDs
                ]
                part_map[effect_name] = LEDEffect(
                    id=effect.id, name=effect_name, effect=bulb_data
                )

    return led_map


# WARNING: Untested
def effect_list_data_sub_to_query(data: SubEffectListItemData) -> QueryEffectListItem:
    effectListItem = QueryEffectListItem(
        start=data.start,
        end=data.end,
        description=data.description,
        id=data.id,
        controlFrames=[],
        positionFrames=[],
    )

    effectListItem.controlFrames = [
        QueryEffectListControlFrame(
            id=controlFrame.id, start=controlFrame.start, fade=controlFrame.fade
        )
        for controlFrame in data.controlFrames
    ]
    effectListItem.positionFrames = [
        QueryEffectListPositionFrame(id=positionFrame.id, start=positionFrame.start)
        for positionFrame in data.positionFrames
    ]

    return effectListItem


def led_record_sub_to_state_item(led_payload_item: SubLEDRecordDataItem) -> LEDEffect:
    effect = [
        LEDBulbData(color_id=bulb[0], alpha=bulb[1])
        for bulb in led_payload_item.frames[0].LEDs
    ]
    return LEDEffect(id=led_payload_item.id, name=led_payload_item.name, effect=effect)


def rgb_to_float(rgb: tuple[int, ...]) -> tuple[float, ...]:
    return tuple([color / 255 for color in rgb])


def float_to_rgb(color_float: tuple[float, ...]) -> tuple[int, ...]:
    return tuple([round(color * 255) for color in color_float])


def rgba_to_float(rgb: tuple[int, ...] | list[int], a: int) -> tuple[float, ...]:
    r, g, b = rgb
    a_float = a / 255
    return (
        r / 255 * a_float,
        g / 255 * a_float,
        b / 255 * a_float,
    )


def is_color_code(color_code: str) -> bool:
    if len(color_code) != 7:
        return False
    if color_code[0] != "#":
        return False
    for char in color_code[1:8]:
        if char not in "1234567890abcdef":
            return False
    return True


def frame_to_time(frame: int) -> str:
    milliseconds = frame
    seconds = milliseconds // 1000
    minutes = seconds // 60
    return f"{minutes:02}:{seconds % 60:02}:{milliseconds % 1000:03}"


def time_to_frame(time: str) -> int:
    splits = time.split(":")
    if len(splits) != 3:
        return -1

    minutes = int(splits[0])
    seconds = int(splits[1])
    milliseconds = int(splits[2])

    return (minutes * 60 + seconds) * 1000 + milliseconds


PosDeleteCurveData = list[int]
PosUpdateCurveData = list[tuple[int, int, tuple[float, float, float]]]
PosAddCurveData = list[tuple[int, tuple[float, float, float]]]

PosModifyAnimationData = dict[
    DancerName, tuple[PosDeleteCurveData, PosUpdateCurveData, PosAddCurveData]
]


def pos_modify_to_animation_data(
    pos_delete: list[tuple[int, MapID]],
    pos_update: list[tuple[int, MapID, PosMapElement]],
    pos_add: list[tuple[MapID, PosMapElement]],
) -> PosModifyAnimationData:
    new_map: PosModifyAnimationData = {}
    for dancer in state.dancers_array:
        new_map[dancer.name] = ([], [], [])

    for old_start, _ in pos_delete:
        for _, dancer_item in enumerate(state.dancers_array):
            dancer = dancer_item.name
            new_map[dancer_item.name][0].append(old_start)

    for old_start, _, frame in pos_update:
        pos_status = frame.pos
        for _, dancer_item in enumerate(state.dancers_array):
            pos = pos_status[dancer_item.name]
            dancer = dancer_item.name
            new_map[dancer_item.name][1].append(
                (old_start, frame.start, (pos.x, pos.y, pos.z))
            )

    for _, frame in pos_add:
        pos_status = frame.pos
        for _, dancer_item in enumerate(state.dancers_array):
            pos = pos_status[dancer_item.name]
            dancer = dancer_item.name
            new_map[dancer_item.name][2].append((frame.start, (pos.x, pos.y, pos.z)))

    return new_map


ControlAnimationData = dict[
    DancerName,
    dict[
        PartName,
        (
            list[tuple[int, bool, tuple[float, float, float]]]
            | list[list[tuple[int, bool, tuple[float, float, float]]]]
        ),
    ],
]

ControlDeleteCurveData = list[int]
ControlUpdateCurveData = list[tuple[int, int, bool, tuple[float, float, float]]]
ControlAddCurveData = list[tuple[int, bool, tuple[float, float, float]]]

ControlModifyAnimationData = dict[
    DancerName,
    dict[
        PartName,
        (
            tuple[
                ControlDeleteCurveData,
                ControlUpdateCurveData,
                ControlAddCurveData,
            ]
            | list[
                tuple[
                    ControlDeleteCurveData,
                    ControlUpdateCurveData,
                    ControlAddCurveData,
                ]
            ]
        ),
    ],
]

ControlUpdateAnimationData = dict[
    DancerName,
    dict[
        PartName,
        ControlUpdateCurveData | list[ControlUpdateCurveData],
    ],
]

ControlDeleteAnimationData = dict[
    DancerName,
    dict[PartName, ControlDeleteCurveData | list[ControlDeleteCurveData]],
]

ControlAddAnimationData = dict[
    DancerName,
    dict[PartName, ControlAddCurveData | list[ControlAddCurveData]],
]


def control_modify_to_animation_data(
    control_delete: list[tuple[int, MapID]],
    control_update: list[tuple[int, MapID, ControlMapElement]],
    control_add: list[tuple[MapID, ControlMapElement]],
) -> ControlModifyAnimationData:
    new_map: ControlModifyAnimationData = {}
    for dancer_name in state.dancers_array:
        new_map[dancer_name.name] = {}
        for part in dancer_name.parts:
            if part.type == PartType.LED:
                length = cast(int, part.length)
                new_map[dancer_name.name][part.name] = [
                    ([], [], []) for _ in range(length)
                ]
            else:
                new_map[dancer_name.name][part.name] = ([], [], [])

    color_map = state.color_map
    led_effect_table = state.led_effect_id_table
    prev_effect_ids: dict[DancerName, dict[PartName, list[int]]] = {}

    for old_start, _ in control_delete:
        for _, dancer_item in enumerate(state.dancers_array):
            dancer_name = dancer_item.name
            parts = dancer_item.parts

            for _, part in enumerate(parts):
                part_name = part.name
                part_map = new_map[dancer_name][part_name]

                if part.type == PartType.LED:
                    part_length = cast(int, part.length)

                    for i in range(part_length):
                        part_map[i][0].append(old_start)  # type: ignore

                else:
                    part_map[0].append(old_start)  # type: ignore

    for old_start, _, frame in control_update:
        for _, dancer_item in enumerate(state.dancers_array):
            dancer_name = dancer_item.name
            parts = dancer_item.parts

            for _, part in enumerate(parts):
                part_name = part.name
                part_map = new_map[dancer_name][part_name]

                part_data = frame.status[dancer_name][part_name]
                part_alpha = part_data.alpha

                if isinstance(part_data, LEDData):
                    part_length = cast(int, part.length)
                    prev_effect_id = prev_effect_ids.setdefault(
                        dancer_name, {}
                    ).setdefault(part_name, [-1])

                    led_rgb_floats = []
                    if part_data.effect_id > 0:
                        part_effect = led_effect_table[part_data.effect_id].effect
                        led_rgb_floats = [
                            rgba_to_float(color_map[led_data.color_id].rgb, part_alpha)
                            for led_data in part_effect
                        ]

                        prev_effect_id[0] = part_data.effect_id

                    elif prev_effect_id[0] > 0:
                        prev_effect = led_effect_table[prev_effect_id[0]].effect
                        led_rgb_floats = [
                            rgba_to_float(color_map[led_data.color_id].rgb, part_alpha)
                            for led_data in prev_effect
                        ]

                    else:
                        led_rgb_floats = [(0, 0, 0)] * part_length

                    for i in range(part_length):
                        part_map[i][1].append((old_start, frame.start, frame.fade, led_rgb_floats[i]))  # type: ignore

                else:
                    part_rgb = color_map[part_data.color_id].rgb
                    fiber_rgb_float = rgba_to_float(part_rgb, part_data.alpha)

                    part_map[1].append((old_start, frame.start, frame.fade, fiber_rgb_float))  # type: ignore

    for _, frame in control_add:
        for _, dancer_item in enumerate(state.dancers_array):
            dancer_name = dancer_item.name
            parts = dancer_item.parts

            for _, part in enumerate(parts):
                part_name = part.name
                part_map = new_map[dancer_name][part_name]

                part_data = frame.status[dancer_name][part_name]
                part_alpha = part_data.alpha

                if isinstance(part_data, LEDData):
                    part_length = cast(int, part.length)
                    prev_effect_id = prev_effect_ids.setdefault(
                        dancer_name, {}
                    ).setdefault(part_name, [-1])

                    led_rgb_floats = []
                    if part_data.effect_id > 0:
                        part_effect = led_effect_table[part_data.effect_id].effect
                        led_rgb_floats = [
                            rgba_to_float(color_map[led_data.color_id].rgb, part_alpha)
                            for led_data in part_effect
                        ]

                        prev_effect_id[0] = part_data.effect_id

                    elif prev_effect_id[0] > 0:
                        prev_effect = led_effect_table[prev_effect_id[0]].effect
                        led_rgb_floats = [
                            rgba_to_float(color_map[led_data.color_id].rgb, part_alpha)
                            for led_data in prev_effect
                        ]

                    else:
                        led_rgb_floats = [(0, 0, 0)] * part_length

                    if len(part_map) == 0:
                        part_map.extend([[] for _ in range(part_length)])  # type: ignore

                    for i in range(part_length):
                        part_map[i][2].append((frame.start, frame.fade, led_rgb_floats[i]))  # type: ignore

                else:
                    part_rgb = color_map[part_data.color_id].rgb
                    fiber_rgb_float = rgba_to_float(part_rgb, part_data.alpha)

                    part_map[2].append((frame.start, frame.fade, fiber_rgb_float))  # type: ignore

    return new_map


def control_add_to_animation_data(
    control_add: list[tuple[MapID, ControlMapElement]],
) -> ControlAddAnimationData:
    new_map: ControlAddAnimationData = {}
    for dancer_name in state.dancers_array:
        new_map[dancer_name.name] = {}
        for part_name in dancer_name.parts:
            new_map[dancer_name.name][part_name.name] = []

    color_map = state.color_map
    led_effect_table = state.led_effect_id_table
    prev_effect_ids: dict[DancerName, dict[PartName, list[int]]] = {}

    for _, frame in control_add:
        for _, dancer_item in enumerate(state.dancers_array):
            dancer_name = dancer_item.name
            parts = dancer_item.parts

            for _, part in enumerate(parts):
                part_name = part.name
                part_map = new_map[dancer_name][part_name]

                part_data = frame.status[dancer_name][part_name]
                part_alpha = part_data.alpha

                if isinstance(part_data, LEDData):
                    part_length = cast(int, part.length)
                    prev_effect_id = prev_effect_ids.setdefault(
                        dancer_name, {}
                    ).setdefault(part_name, [-1])

                    led_rgb_floats = []
                    if part_data.effect_id > 0:
                        part_effect = led_effect_table[part_data.effect_id].effect
                        led_rgb_floats = [
                            rgba_to_float(color_map[led_data.color_id].rgb, part_alpha)
                            for led_data in part_effect
                        ]

                        prev_effect_id[0] = part_data.effect_id

                    elif prev_effect_id[0] > 0:
                        prev_effect = led_effect_table[prev_effect_id[0]].effect
                        led_rgb_floats = [
                            rgba_to_float(color_map[led_data.color_id].rgb, part_alpha)
                            for led_data in prev_effect
                        ]

                    else:
                        led_rgb_floats = [(0, 0, 0)] * part_length

                    if len(part_map) == 0:
                        part_map.extend([[] for _ in range(part_length)])  # type: ignore

                    for i in range(part_length):
                        part_map[i].append((frame.start, frame.fade, led_rgb_floats[i]))  # type: ignore

                else:
                    part_rgb = color_map[part_data.color_id].rgb
                    fiber_rgb_float = rgba_to_float(part_rgb, part_data.alpha)

                    part_map.append((frame.start, frame.fade, fiber_rgb_float))  # type: ignore

    return new_map


def control_delete_to_animation_data(
    control_delete: list[tuple[int, MapID]]
) -> ControlDeleteAnimationData:
    new_map: ControlDeleteAnimationData = {}
    for dancer_name in state.dancers_array:
        new_map[dancer_name.name] = {}
        for part_name in dancer_name.parts:
            new_map[dancer_name.name][part_name.name] = []

    for old_start, _ in control_delete:
        for _, dancer_item in enumerate(state.dancers_array):
            dancer_name = dancer_item.name
            parts = dancer_item.parts

            for _, part in enumerate(parts):
                part_name = part.name
                part_map = new_map[dancer_name][part_name]

                if part.type == PartType.LED:
                    part_length = cast(int, part.length)

                    if len(part_map) == 0:
                        part_map.extend([[] for _ in range(part_length)])  # type: ignore

                    for i in range(part_length):
                        part_map[i].append(old_start)  # type: ignore

                else:
                    part_map.append(old_start)  # type: ignore

    return new_map


def control_update_to_animation_data(
    control_update: list[tuple[int, MapID, ControlMapElement]],
) -> ControlUpdateAnimationData:
    new_map: ControlUpdateAnimationData = {}
    for dancer_name in state.dancers_array:
        new_map[dancer_name.name] = {}
        for part_name in dancer_name.parts:
            new_map[dancer_name.name][part_name.name] = []

    color_map = state.color_map
    led_effect_table = state.led_effect_id_table
    prev_effect_ids: dict[DancerName, dict[PartName, list[int]]] = {}

    for old_start, _, frame in control_update:
        for _, dancer_item in enumerate(state.dancers_array):
            dancer_name = dancer_item.name
            parts = dancer_item.parts

            for _, part in enumerate(parts):
                part_name = part.name
                part_map = new_map[dancer_name][part_name]

                part_data = frame.status[dancer_name][part_name]
                part_alpha = part_data.alpha

                if isinstance(part_data, LEDData):
                    part_length = cast(int, part.length)
                    prev_effect_id = prev_effect_ids.setdefault(
                        dancer_name, {}
                    ).setdefault(part_name, [-1])

                    led_rgb_floats = []
                    if part_data.effect_id > 0:
                        part_effect = led_effect_table[part_data.effect_id].effect
                        led_rgb_floats = [
                            rgba_to_float(color_map[led_data.color_id].rgb, part_alpha)
                            for led_data in part_effect
                        ]

                        prev_effect_id[0] = part_data.effect_id

                    elif prev_effect_id[0] > 0:
                        prev_effect = led_effect_table[prev_effect_id[0]].effect
                        led_rgb_floats = [
                            rgba_to_float(color_map[led_data.color_id].rgb, part_alpha)
                            for led_data in prev_effect
                        ]

                    else:
                        led_rgb_floats = [(0, 0, 0)] * part_length

                    if len(part_map) == 0:
                        part_map.extend([[] for _ in range(part_length)])  # type: ignore

                    for i in range(part_length):
                        part_map[i].append((old_start, frame.start, frame.fade, led_rgb_floats[i]))  # type: ignore

                else:
                    part_rgb = color_map[part_data.color_id].rgb
                    fiber_rgb_float = rgba_to_float(part_rgb, part_data.alpha)

                    part_map.append((old_start, frame.start, frame.fade, fiber_rgb_float))  # type: ignore

    return new_map


# Control map needs to be sorted by start time
def control_map_to_animation_data(
    control_map: list[tuple[MapID, ControlMapElement]],
) -> ControlAnimationData:
    new_map: ControlAnimationData = {}
    for dancer_name in state.dancers_array:
        new_map[dancer_name.name] = {}
        for part_name in dancer_name.parts:
            new_map[dancer_name.name][part_name.name] = []

    color_map = state.color_map
    led_effect_table = state.led_effect_id_table
    prev_effect_ids: dict[DancerName, dict[PartName, list[int]]] = {}

    for _, frame in control_map:
        for _, dancer_item in enumerate(state.dancers_array):
            dancer_name = dancer_item.name
            parts = dancer_item.parts

            for _, part in enumerate(parts):
                part_name = part.name
                part_map = new_map[dancer_name][part_name]

                part_data = frame.status[dancer_name][part_name]
                part_alpha = part_data.alpha

                if isinstance(part_data, LEDData):
                    part_length = cast(int, part.length)
                    prev_effect_id = prev_effect_ids.setdefault(
                        dancer_name, {}
                    ).setdefault(part_name, [-1])

                    led_rgb_floats = []
                    if part_data.effect_id > 0:
                        part_effect = led_effect_table[part_data.effect_id].effect
                        led_rgb_floats = [
                            rgba_to_float(color_map[led_data.color_id].rgb, part_alpha)
                            for led_data in part_effect
                        ]

                        prev_effect_id[0] = part_data.effect_id

                    elif prev_effect_id[0] > 0:
                        prev_effect = led_effect_table[prev_effect_id[0]].effect
                        led_rgb_floats = [
                            rgba_to_float(color_map[led_data.color_id].rgb, part_alpha)
                            for led_data in prev_effect
                        ]

                    else:
                        led_rgb_floats = [(0, 0, 0)] * part_length

                    if len(part_map) == 0:
                        part_map.extend([[] for _ in range(part_length)])  # type: ignore

                    for i in range(part_length):
                        part_map[i].append((frame.start, frame.fade, led_rgb_floats[i]))  # type: ignore

                else:
                    part_rgb = color_map[part_data.color_id].rgb
                    fiber_rgb_float = rgba_to_float(part_rgb, part_data.alpha)

                    part_map.append((frame.start, frame.fade, fiber_rgb_float))  # type: ignore

        # print("Frame: ", frame.start)

    return new_map
