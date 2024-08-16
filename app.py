from flask import Flask, request, jsonify
from kubernetes import client, config
import os

app = Flask(__name__)

# Load Kubernetes config
config.load_incluster_config()
v1 = client.CoreV1Api()

@app.route('/create-pv-pvc', methods=['POST'])
def create_pv_pvc():
    data = request.json
    pvc_name = data.get('name')
    nfs_path = data.get('path')
    pv_capacity = data.get('capacity')
    nfs_server = os.getenv('NFS_SERVER')

    if not pvc_name or not nfs_path or not pv_capacity or not nfs_server:
        return jsonify({"error": "name, path, capacity, and NFS_SERVER are required"}), 400

    access_modes = ["ReadWriteMany"]

    try:
        # Create PV
        pv_name = f"{pvc_name}-pv"
        pv_body = client.V1PersistentVolume(
            metadata=client.V1ObjectMeta(name=pv_name),
            spec=client.V1PersistentVolumeSpec(
                capacity={"storage": pv_capacity},
                access_modes=access_modes,
                nfs=client.V1NFSVolumeSource(
                    path=nfs_path,
                    server=nfs_server
                ),
                persistent_volume_reclaim_policy="Retain",
            )
        )
        v1.create_persistent_volume(pv_body)

        # Create PVC
        pvc_body = client.V1PersistentVolumeClaim(
            metadata=client.V1ObjectMeta(name=pvc_name),
            spec=client.V1PersistentVolumeClaimSpec(
                access_modes=access_modes,
                resources=client.V1ResourceRequirements(
                    requests={"storage": pv_capacity}
                ),
                volume_name=pv_name
            )
        )
        v1.create_namespaced_persistent_volume_claim(namespace="default", body=pvc_body)

        return jsonify({"message": f"PV and PVC '{pvc_name}' created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)