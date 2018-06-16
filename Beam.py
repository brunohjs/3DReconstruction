

'Classe que representa um bin do sonar MSIS'
class Beam:
    def __init__(self, line):
        self.frame = int(line[0])
        self.angle_head = float(line[1])
        
        self.position_x = float(line[2])
        self.position_y = float(line[3])
        self.position_z = float(line[4])

        self.orientation_x = float(line[5])
        self.orientation_y = float(line[6])
        self.orientation_z = float(line[7])
        self.orientation_w = float(line[8])

        (self.angular_x, 
        self.angular_y, 
        self.angular_z) = quaternion2Euler(
            self.orientation_x, 
            self.orientation_y,
            self.orientation_z,
            self.orientation_w)
        
        self.bins = convertRaw(list(line[9:-1]))
        self.higher = max(self.bins)

    def getDistance(self):
        