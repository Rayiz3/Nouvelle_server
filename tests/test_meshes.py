def test_add_mesh(meshes_client):
    response = meshes_client.post('/meshes',
        query_string={"id": '1234'},
        json={"prompt": "a cute cat"}
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["message"] == "Mesh created successful"
    assert data["iconMeshUrl"] == "https://pub-example.r2.dev/newmesh.glb"