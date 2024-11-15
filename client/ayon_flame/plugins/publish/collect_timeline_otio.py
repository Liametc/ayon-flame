import pyblish.api
from pprint import pformat

import ayon_flame.api as ayfapi
from ayon_flame.otio import flame_export


class CollecTimelineOTIO(pyblish.api.ContextPlugin):
    """Inject the current working context into publish context"""

    label = "Collect Timeline OTIO"
    order = pyblish.api.CollectorOrder - 0.099

    def process(self, context):

        # main
        project = ayfapi.get_current_project()
        sequence = ayfapi.get_current_sequence(ayfapi.CTX.selection)


        # adding otio timeline to context
        with ayfapi.maintained_segment_selection(sequence) as selected_seg:
            otio_timeline = flame_export.create_otio_timeline(sequence)

            # update context with main project attributes
            timeline_data = {
                "flameProject": project,
                "flameSequence": sequence,
                "otioTimeline": otio_timeline,
                "currentFile": "Flame/{}/{}".format(
                    project.name, sequence.name.get_value()
                ),
                "flameSelectedSegments": selected_seg,
                "fps": float(str(sequence.frame_rate)[:-4])
            }
            self.log.debug(f">>> Timeline data: {pformat(timeline_data)}")
            context.data.update(timeline_data)
