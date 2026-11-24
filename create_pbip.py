"""
Generate Power BI Project (.pbip) for Skyworth & Philips TV Review Operations
Enables direct 1-click launch in modern Power BI Desktop with full layout, measures, and datasets.
"""

import os
import json
import zipfile

def build_pbip():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pbit_path = os.path.join(base_dir, 'Skyworth_Review_Operations.pbit')

    if not os.path.exists(pbit_path):
        print("Skyworth_Review_Operations.pbit not found, please generate it first.")
        return

    with zipfile.ZipFile(pbit_path, 'r') as z:
        dms_str = z.read('DataModelSchema').decode('utf-16le', errors='ignore')
        layout_str = z.read('Report/Layout').decode('utf-16le', errors='ignore')

    model_data = json.loads(dms_str)
    layout_data = json.loads(layout_str)

    pbip_path = os.path.join(base_dir, 'Skyworth_Review_Operations.pbip')
    report_dir = os.path.join(base_dir, 'Skyworth_Review_Operations.Report')
    model_dir = os.path.join(base_dir, 'Skyworth_Review_Operations.SemanticModel')

    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)

    # 1. Root .pbip
    with open(pbip_path, 'w', encoding='utf-8') as f:
        json.dump({
            'version': '1.0',
            'artifacts': [{'report': {'path': 'Skyworth_Review_Operations.Report'}}],
            'settings': {'enableAutoAuth': True}
        }, f, indent=2)

    # 2. Report definition.pbir
    with open(os.path.join(report_dir, 'definition.pbir'), 'w', encoding='utf-8') as f:
        json.dump({
            'version': '4.0',
            'datasetReference': {
                'byPath': {'path': '../Skyworth_Review_Operations.SemanticModel'},
                'byConnection': None
            }
        }, f, indent=2)

    # 3. Report report.json
    with open(os.path.join(report_dir, 'report.json'), 'w', encoding='utf-8') as f:
        json.dump(layout_data, f, indent=2)

    # 4. SemanticModel definition.pbism
    with open(os.path.join(model_dir, 'definition.pbism'), 'w', encoding='utf-8') as f:
        json.dump({'version': '4.0'}, f, indent=2)

    # 5. SemanticModel model.bim
    with open(os.path.join(model_dir, 'model.bim'), 'w', encoding='utf-8') as f:
        json.dump(model_data, f, indent=2)

    print(f"Successfully generated Power BI Project: {pbip_path}")

if __name__ == '__main__':
    build_pbip()
