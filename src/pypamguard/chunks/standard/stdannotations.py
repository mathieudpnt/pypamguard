from pypamguard.core.serializable import Serializable
import pypamguard.chunks.annotations as annotations
from pypamguard.chunks.base import BaseChunk
from pypamguard.core.readers import *
from pypamguard.core.exceptions import StructuralException

annotation_types = {
    'Beer': annotations.BeamFormerAnnotation,
    'Bearing': annotations.BearingAnnotation,
    'TMAN': annotations.TMAnnotation,
    'TBDL': annotations.TBDLAnnotation,
    'ClickClassifier_1': annotations.ClickClsfrAnnotation,
    'Matched_Clk_Clsfr': annotations.MatchClsfrAnnotation,
    'BCLS': annotations.RWUDPAnnotation,
    'DLRE': annotations.DLAnnotation,
    'Delt': annotations.DLAnnotation,
    'Uson': annotations.UserFormAnnotation,
    'USON': annotations.UserFormAnnotation,
}

class StdAnnotations(BaseChunk):

    beam_angles: annotations.BeamFormerAnnotation
    bearing: annotations.BearingAnnotation
    target_motion: annotations.TMAnnotation
    toad_angles: annotations.TBDLAnnotation
    classification: annotations.ClickClsfrAnnotation
    m_classification: annotations.MatchClsfrAnnotation
    basic_classification: annotations.RWUDPAnnotation
    dl_classification: annotations.DLAnnotation
    user_form_data: annotations.UserFormAnnotation

    def _process(self, br, *args, **kwargs):
        annotations_length = br.bin_read(DTYPES.INT16)
        n_annotations = br.bin_read(DTYPES.INT16)
        for i in range(n_annotations):
            annotation_length = br.bin_read(DTYPES.INT16) - 2
            annotation_id = br.string_read()
            annotation_version = br.bin_read(DTYPES.INT16)
            kwarg_data = {
                "annotation_length": annotation_length,
                "annotation_id": annotation_id,
                "annotation_version": annotation_version,
            }
            
            if annotation_id == 'Beer':
                self.beam_angles = annotations.BeamFormerAnnotation()
                self.beam_angles.process(br, *args, **kwarg_data)
            elif annotation_id == 'Bearing':
                self.bearing = annotations.BearingAnnotation()
                self.bearing.process(br, *args, **kwarg_data)
            elif annotation_id == 'TMAN':
                self.target_motion = annotations.TMAnnotation()
                self.target_motion.process(br, *args, **kwarg_data)
            elif annotation_id == 'TBDL':
                self.toad_angles = annotations.TBDLAnnotation()
                self.toad_angles.process(br, *args, **kwarg_data)
            elif annotation_id == 'ClickClassifier_1':
                self.classification = annotations.ClickClsfrAnnotation()
                self.classification.process(br, *args, **kwarg_data)
            elif annotation_id == 'Matched_Clk_Clsfr':
                self.m_classification = annotations.MatchClsfrAnnotation()
                self.m_classification.process(br, *args, **kwarg_data)
            elif annotation_id == 'BCLS':
                self.basic_classification = annotations.RWUDPAnnotation()
                self.basic_classification.process(br, *args, **kwarg_data)
            elif annotation_id == 'DLRE' or annotation_id == 'Delt':
                self.dl_classification = annotations.DLAnnotation()
                self.dl_classification.process(br, *args, **kwarg_data)
            elif annotation_id == 'Uson' or annotation_id == 'USON':
                self.user_form_data = annotations.UserFormAnnotation()
                self.user_form_data.process(br, *args, **kwarg_data)
            elif annotation_id == 'USON':
                self.user_form_data = annotations.UserFormAnnotation()
                self.user_form_data.process(br, *args, **kwarg_data)
            else:
                raise Exception(f"Unknown annotation type: {annotation_id}")
