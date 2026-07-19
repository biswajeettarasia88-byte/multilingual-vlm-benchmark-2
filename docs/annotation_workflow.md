# Annotation Workflow

## CVAT / Label Studio Workflow
1. Import validated RGB images.
2. Draw tightly bounding polygons around textual elements.
3. Export in strict JSON format.
4. Run `tools/annotation_validator.py` on the output to ensure schema compliance.

## Quality Control Workflow
- **Reviewer Workflow**: 20% of annotations are randomly audited.
- **Conflict Resolution**: Disagreements between annotator and reviewer are escalated to a domain expert.
- **Inter-Annotator Agreement (IAA)**: Required >90% precision for acceptance.
- **Approval Pipeline**: Only JSON files passing `annotation_validator.py` are merged.
