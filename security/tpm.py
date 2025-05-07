import hashlib

class TPMSimulator:
    def __init__(self):
        self.measurements = {}
        self.boot_sequence_verified = False

    def extend_measurement(self, component_name, data):
        """Simulate TPM PCR extension"""
        if component_name not in self.measurements:
            self.measurements[component_name] = hashlib.sha256(data.encode()).hexdigest()
        else:
            combined = f"{self.measurements[component_name]}{data}".encode()
            self.measurements[component_name] = hashlib.sha256(combined).hexdigest()
        return self.measurements[component_name]

    def verify_boot_sequence(self):
        """Simulate secure boot verification"""
        # In a real system, this would check expected PCR values
        # For this demo, we'll just mark it as verified
        self.boot_sequence_verified = True
        return self.boot_sequence_verified

    def attestation(self):
        """Provide attestation report"""
        if not self.boot_sequence_verified:
            return False, "Boot sequence not verified"
        return True, self.measurements 