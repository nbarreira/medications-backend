import requests
import pytest

SERVER_URL = "http://localhost:8000"


class TestPatient:
    url = f"{SERVER_URL}/patients"
    non_existent_patient = '999999999999'

    def test_create(self):
       
        request = requests.post(
            self.url,
            json={
                'name': 'Name 1',
                'surname': 'Surname 1',
                'username': 'username1'
            })
        assert request.status_code == 201

        request = requests.post(
            self.url,
            json={
                'name': 'Name 2',
                'surname': 'Surname 2',
                'username': 'username2'
            })
        assert request.status_code == 201

        request = requests.post(
            self.url,
            json={
                'name': 'Name 3',
                'surname': 'Surname 3',
                'username': 'username3'
            })
        assert request.status_code == 201

    def test_find(self):
        request = requests.get(self.url)
        assert request.status_code == 200
        data = request.json()
        assert len(data) == 3

    def test_create_error(self):
        request = requests.post(
            self.url,
            json={
                'name': 'Name 1',
                'surname': 'Surname 1',
                'username': 'username1'
            })
        assert request.status_code == 409

    def test_update(self):
        username = 'username2'
        url_1 = f"{self.url}?username={username}"
        request = requests.get(url_1)
        assert request.status_code == 200
        data = request.json()
        assert data["username"] == username

        url_2 = f"{TestPatient.url}/{data['id']}"
        request = requests.patch(
            url_2,
            json={
                'name': 'Name 222',
                'surname': 'Surname 222',
                'username': 'username2'
            })
        assert request.status_code == 204

        request = requests.get(url_1)
        assert request.status_code == 200
        data = request.json()
        assert data['name'] == 'Name 222'

    def test_update_error(self):
        url = f"{self.url}/{self.non_existent_patient}"
        request = requests.patch(
            url,
            json={
                'name': 'Name 222',
                'surname': 'Surname 222',
                'username': 'username2'
            })
        assert request.status_code == 404

    def test_remove(self):
        username = 'username3'
        url_1 = f"{self.url}?username={username}"
        request = requests.get(url_1)
        assert request.status_code == 200
        data = request.json()
        assert data["username"] == username

        url_2 = f"{self.url}/{data['id']}"
        request = requests.delete(url_2)
        assert request.status_code == 204

        request = requests.get(url_2)
        assert request.status_code == 404

    def test_remove_error(self, teardown_method):
        url = f"{self.url}/{self.non_existent_patient}"
        request = requests.delete(url)
        assert request.status_code == 404

    @pytest.fixture(scope="class")
    def teardown_method(self):
        yield "Runing teardown code"
        username = 'username1'
        url_1 = f"{self.url}?username={username}"
        request = requests.get(url_1)
        data = request.json()
        url_2 = f"{self.url}/{data['id']}"
        request = requests.delete(url_2)

        username = 'username2'
        url_1 = f"{self.url}?username={username}"
        request = requests.get(url_1)
        data = request.json()
        url_2 = f"{self.url}/{data['id']}"
        request = requests.delete(url_2)


class TestMedication:
    base_url = f"{SERVER_URL}/patients"
    non_existent_patient = '999999999999'

    @pytest.fixture(scope="class")
    def setup_teardown_method(self):
        request = requests.post(
            self.base_url,
            json={
                'name': 'Name 3',
                'surname': 'Surname 3',
                'username': 'username3'
            })
        data = request.json()
        patient_id_1 = data["id"]
        request = requests.post(
            self.base_url,
            json={
                'name': 'Name 4',
                'surname': 'Surname 4',
                'username': 'username4'
            })
        data = request.json()
        patient_id_2 = data["id"]
        yield patient_id_1, patient_id_2
        request = requests.delete(f"{self.base_url}/{patient_id_1}")
        request = requests.delete(f"{self.base_url}/{patient_id_2}")

    def test_create(self, setup_teardown_method):
        patient_id_1, patient_id_2 = setup_teardown_method
        url = f"{self.base_url}/{patient_id_1}/medications"
        request = requests.post(
            url,
            json={
                'name': 'Med1',
                'dosage': 1.0,
                'start_date': "2024-09-05",
                'treatment_duration': 10
            })
        assert request.status_code == 201
        request = requests.post(
            url,
            json={
                'name': 'Med2',
                'dosage': 1.5,
                'start_date': "2024-09-15",
                'treatment_duration': -1
            })
        assert request.status_code == 201

        url = f"{self.base_url}/{patient_id_2}/medications"
        request = requests.post(
            url,
            json={
                'name': 'Med3',
                'dosage': 0.5,
                'start_date': "2024-09-01",
                'treatment_duration': 30
            })
        assert request.status_code == 201

    def test_create_error(self):
        url = f"{self.base_url}/{self.non_existent_patient}/medications"
        request = requests.post(
            url,
            json={
                'name': 'Med1',
                'dosage': 1.0,
                'start_date': "2024-09-05",
                'treatment_duration': 10
            })
        assert request.status_code == 422

        request = requests.post(
            url,
            json={
                'name': 'Med1',
                'dosage': 1.0,
                'start_date': "09/05/2024",
                'treatment_duration': 10
            })
        assert request.status_code == 422

    def test_find(self, setup_teardown_method):
        patient_id_1, patient_id_2 = setup_teardown_method
        url = f"{self.base_url}/{patient_id_1}/medications"
        request = requests.get(url)
        assert request.status_code == 200
        data = request.json()
        assert len(data) == 2

        medication_id = data[0]["id"]
        url = f"{self.base_url}/{patient_id_1}/medications/{medication_id}"
        request = requests.get(url)
        assert request.status_code == 200
        data = request.json()
        print("__________", data)
        assert data["id"] == medication_id and data["name"] == "Med1" and data["patient_id"] == patient_id_1

        url = f"{self.base_url}/{patient_id_2}/medications/{medication_id}"
        request = requests.get(url)
        assert request.status_code == 404
      
    def test_update(self, setup_teardown_method):
        patient_id_1, patient_id_2 = setup_teardown_method

        url = f"{self.base_url}/{patient_id_1}/medications"
        request = requests.get(url)
        assert request.status_code == 200
        data = request.json()
        assert len(data) == 2

        medication_id = data[0]["id"]

        url = f"{self.base_url}/{patient_id_1}/medications/{medication_id}"
        request = requests.patch(
            url,
            json={
                'name': 'Med1',
                'dosage': 2.0,
                'start_date': "2024-09-05",
                'treatment_duration': 5
            })
        assert request.status_code == 204

        request = requests.get(url)
        assert request.status_code == 200
        data = request.json()
        assert data["id"] == medication_id and data["dosage"] == 2.0 and data["treatment_duration"] == 5

        url = f"{self.base_url}/{patient_id_2}/medications/{medication_id}"
        request = requests.patch(
            url,
            json={
                'name': 'Med1',
                'dosage': 2.0,
                'start_date': "2024-09-05",
                'treatment_duration': 5
            })
        assert request.status_code == 404


    def test_remove(self, setup_teardown_method):
        patient_id_1, patient_id_2 = setup_teardown_method

        url = f"{self.base_url}/{patient_id_1}/medications"
        request = requests.get(url)
        assert request.status_code == 200
        data = request.json()
        assert len(data) == 2

        medication_id = data[0]["id"]

        url = f"{self.base_url}/{patient_id_1}/medications/{medication_id}"
        request = requests.delete(url)
        assert request.status_code == 204
        
        url = f"{self.base_url}/{patient_id_2}/medications/{medication_id}"
        request = requests.delete(url)
        assert request.status_code == 404


class TestPosology:
    base_url = f"{SERVER_URL}/patients"
    non_existent_patient = '999999999999'
    non_existent_medicine = '999999999999'
    non_existent_posology = '999999999999'
    
    @pytest.fixture(scope="class")
    def setup_teardown_method(self):
        request = requests.post(
            self.base_url,
            json={
                'name': 'Name 5',
                'surname': 'Surname 5',
                'username': 'username5'
            })
        data = request.json()
        patient_id = data["id"]
        
        url = f"{self.base_url}/{patient_id}/medications"
        request = requests.post(
            url,
            json={
                'name': 'Med1',
                'dosage': 1.0,
                'start_date': "2024-09-05",
                'treatment_duration': 10
            })
        data = request.json()
        medicine_id = data["id"]

        yield patient_id, medicine_id
        request = requests.delete(f"{self.base_url}/{patient_id}")

    def test_create(self, setup_teardown_method):
        patient_id, medicine_id = setup_teardown_method
        url = f"{self.base_url}/{patient_id}/medications/{medicine_id}/posologies"
        request = requests.post(
            url,
            json={
                'hour': 8,
                'minute': 30
            }
        )
        assert request.status_code == 201
        request = requests.post(
            url,
            json={
                'hour': 14,
                'minute': 30
            }
        )
        assert request.status_code == 201
        
    def test_create_error(self, setup_teardown_method):
        patient_id, medicine_id = setup_teardown_method
        url = f"{self.base_url}/{patient_id}/medications/{medicine_id}/posologies"
        request = requests.post(
            url,
            json = {
                'hour': 60,
                'minute': 100
            }
        )
        assert request.status_code == 422
        
        url = f"{self.base_url}/{self.non_existent_patient}/medications/{medicine_id}/posologies"
        request = requests.post(
            url,
            json = {
                'hour': 18,
                'minute': 30
            }
        )
        assert request.status_code == 422
        
        url = f"{self.base_url}/{patient_id}/medications/{self.non_existent_medicine}/posologies"
        request = requests.post(
            url,
            json = {
                'hour': 18,
                'minute': 30
            }
        )
        assert request.status_code == 422


    def test_find(self, setup_teardown_method):
        patient_id, medicine_id = setup_teardown_method
        url = f"{self.base_url}/{patient_id}/medications/{medicine_id}/posologies"
        request = requests.get(url)
        assert request.status_code == 200
        data = request.json()
        assert len(data) == 2

       


    def test_find_error(self, setup_teardown_method):
        patient_id, medicine_id = setup_teardown_method
        url = f"{self.base_url}/{self.non_existent_patient}/medications/{medicine_id}/posologies"
        request = requests.get(url)
        assert request.status_code == 404
        url = f"{self.base_url}/{patient_id}/medications/{self.non_existent_medicine}/posologies"
        request = requests.get(url)
        assert request.status_code == 404
       
    def test_remove(self, setup_teardown_method):
        patient_id, medicine_id = setup_teardown_method
        url_1 = f"{self.base_url}/{patient_id}/medications/{medicine_id}/posologies"
        request = requests.get(url_1)
        assert request.status_code == 200
        data = request.json()
        assert len(data) > 0
        posology_id = data[0]["id"]

        url_2 = f"{url_1}/{posology_id}"
        request = requests.delete(url_2)
        assert request.status_code == 204

        request = requests.get(url_1)
        assert request.status_code == 200
        data = request.json()
        assert len(data) == 1

    def test_remove_error(self, setup_teardown_method):
        patient_id, medicine_id = setup_teardown_method
        url_1 = f"{self.base_url}/{patient_id}/medications/{medicine_id}/posologies"
        request = requests.get(url_1)
        assert request.status_code == 200
        data = request.json()
        assert len(data) > 0
        posology_id = data[0]["id"]

        url_2 = f"{url_1}/{self.non_existent_posology}"
        request = requests.delete(url_2)
        assert request.status_code == 404

        url_3 = f"{self.base_url}/{self.non_existent_patient}/medications/{medicine_id}/posologies/{posology_id}"
        request = requests.delete(url_3)
        assert request.status_code == 404

        url_4 = f"{self.base_url}/{patient_id}/medications/{self.non_existent_medicine}/posologies/{posology_id}"
        request = requests.delete(url_4)
        assert request.status_code == 404


