class Patient:
    def __init__(self, patient_name):
        self.name = patient_name
        self.exams = []

    def add_exam(self, exam):
        self.exams.append(exam)

    def remove_exam(self, exam):
        self.exams.remove(exam)

    def get_num_exams(self):
        return len(self.exams)

class DataAggregator:
    def __init__(self, filename):
        self.filename = filename
        self.parsed_data = self.read_file(self.filename)
        self.patients = {}
        self.exam_data = {}

    """
    Reads the contents of a file and returns the lines as a list.
    """
    def read_file(self, file_name):
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()
                return lines
        except FileNotFoundError:
            print("File not found.")
            return []
        
    """
    Parses the data and performs aggregation.
    """
    def parse_data(self):
        for line in self.parsed_data:
            line = line.strip()
            line = line.split(' ')

            if line[0] == "ADD":
                if line[1] == "PATIENT":
                    patient_id = line[2]

                    if patient_id not in self.patients:
                        #assuming the patient name consists of first name and last name
                        patient_name = line[3] + " " + line[4]
                        self.patients[patient_id] = Patient(patient_name)
                elif line[1] == "EXAM":
                    patient_id = line[2]
                    exam_id = line[3]

                    if patient_id in self.patients and exam_id not in self.exam_data:
                        self.exam_data[exam_id] = patient_id
                        self.patients[patient_id].add_exam(exam_id)
            elif line[0] == "DEL":
                if line[1] == "PATIENT":
                    patient_id = line[2]

                    if patient_id in self.patients:
                        # delete any exams associated with the patient
                        for exam in self.patients[patient_id].exams:
                            del self.exam_data[exam]
                        del self.patients[patient_id]
                elif line[1] == "EXAM":
                    exam_id = line[2]

                    if exam_id in self.exam_data:
                        patient_id = self.exam_data[exam_id]
                        self.patients[patient_id].remove_exam(exam_id)
                        del self.exam_data[exam_id]

    """
    Prints summary of patients in system.
    """
    def print_patients(self):
        for patient_id, patient in self.patients.items():
            print("Name: " + patient.name + ", " + "ID: " + str(patient_id) + ", " + 
                  "Exam Count: " + str(patient.get_num_exams()))

    """
    Asks user to input the name of the file.
    """
def get_file_name():
    file_name = input("Enter the name of the file to process (include the .txt): ")
    return file_name

def main():
    file_name = get_file_name()
    data_aggregator = DataAggregator(file_name)
    data_aggregator.parse_data()
    data_aggregator.print_patients()

if __name__ == "__main__":
    main()