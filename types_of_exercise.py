import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose

class BodyPartAngle:
    def __init__(self, landmarks):
        self.landmarks = landmarks

    def detection_body_part(self, body_part):
        return self.landmarks[mp_pose.PoseLandmark[body_part].value]

    def calculate_angle(self, a, b, c):
        a = np.array([a.x, a.y])
        b = np.array([b.x, b.y])
        c = np.array([c.x, c.y])
        
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360.0 - angle
        return angle

    def angle_of_the_left_leg(self):
        l_hip = self.detection_body_part("LEFT_HIP")
        l_knee = self.detection_body_part("LEFT_KNEE")
        l_ankle = self.detection_body_part("LEFT_ANKLE")
        return self.calculate_angle(l_hip, l_knee, l_ankle)

    def angle_of_the_right_leg(self):
        r_hip = self.detection_body_part("RIGHT_HIP")
        r_knee = self.detection_body_part("RIGHT_KNEE")
        r_ankle = self.detection_body_part("RIGHT_ANKLE")
        return self.calculate_angle(r_hip, r_knee, r_ankle)

    def angle_of_the_left_arm(self):
        l_shoulder = self.detection_body_part("LEFT_SHOULDER")
        l_elbow = self.detection_body_part("LEFT_ELBOW")
        l_wrist = self.detection_body_part("LEFT_WRIST")
        return self.calculate_angle(l_shoulder, l_elbow, l_wrist)

    def angle_of_the_right_arm(self):
        r_shoulder = self.detection_body_part("RIGHT_SHOULDER")
        r_elbow = self.detection_body_part("RIGHT_ELBOW")
        r_wrist = self.detection_body_part("RIGHT_WRIST")
        return self.calculate_angle(r_shoulder, r_elbow, r_wrist)

    def is_lying_down(self):
        left_shoulder = self.detection_body_part("LEFT_SHOULDER")
        right_shoulder = self.detection_body_part("RIGHT_SHOULDER")
        left_hip = self.detection_body_part("LEFT_HIP")
        right_hip = self.detection_body_part("RIGHT_HIP")
        left_knee = self.detection_body_part("LEFT_KNEE")
        right_knee = self.detection_body_part("RIGHT_KNEE")
        left_ankle = self.detection_body_part("LEFT_ANKLE")
        right_ankle = self.detection_body_part("RIGHT_ANKLE")

        threshold = 0.1

        shoulder_diff = abs(left_shoulder.y - right_shoulder.y)
        hip_diff = abs(left_hip.y - right_hip.y)
        knee_diff = abs(left_knee.y - right_knee.y)
        ankle_diff = abs(left_ankle.y - right_ankle.y)

        if (shoulder_diff < threshold and hip_diff < threshold and
            knee_diff < threshold and ankle_diff < threshold):
            return True
        return False

class TypeOfExercise(BodyPartAngle):
    def __init__(self, landmarks):
        super().__init__(landmarks)
    
    def leg_in_and_outs(self, counter, status):
        left_hip = self.landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = self.landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = self.landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = self.landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_ankle = self.landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = self.landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

        # Bacak açısını hesapla
        left_leg_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        right_leg_angle = self.calculate_angle(right_hip, right_knee, right_ankle)

        # Bacakların 60 dereceden büyük açıyla yukarı kalkmış mı kontrol et
        if left_leg_angle > 60 or right_leg_angle > 60:
            leg_lifted = True
        else:
            leg_lifted = False

        # Hareketin düzgün yapıldığını kontrol et
        if status:
            if leg_lifted:
                counter += 1
                status = False
        else:
            if not leg_lifted:
                status = True

        return [counter, status]

    def leg_lateral(self, counter, status):
        left_hip = self.landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = self.landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = self.landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = self.landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_ankle = self.landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = self.landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

        # Sol bacak açısını hesapla
        left_leg_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        right_leg_angle = self.calculate_angle(right_hip, right_knee, right_ankle)

        # Bacakların aynı anda yukarı kalkmış mı kontrol et
        if (left_knee.y < left_hip.y and left_ankle.y < left_knee.y) or (right_knee.y < right_hip.y and right_ankle.y < right_knee.y):
            leg_lifted = True
        else:
            leg_lifted = False

        # Hareketin düzgün yapıldığını kontrol et
        if status:
            if leg_lifted and (left_leg_angle >= 45 or right_leg_angle >= 45):
                counter += 1
                status = False
        else:
            if not leg_lifted or (left_leg_angle < 45 and right_leg_angle < 45):
                status = True

        return [counter, status]

    def push_up(self, counter, status):
        left_arm_angle = self.angle_of_the_left_arm()
        right_arm_angle = self.angle_of_the_right_arm()
        avg_arm_angle = (left_arm_angle + right_arm_angle) // 2

        if status:
            if avg_arm_angle < 70:
                counter += 1
                status = False
        else:
            if avg_arm_angle > 160:
                status = True

        return [counter, status]

    def pull_up(self, counter, status):
        nose = self.detection_body_part("NOSE")
        left_elbow = self.detection_body_part("LEFT_ELBOW")
        right_elbow = self.detection_body_part("RIGHT_ELBOW")
        avg_shoulder_y = (left_elbow.y + right_elbow.y) / 2

        if status:
            if nose.y > avg_shoulder_y:
                counter += 1
                status = False
        else:
            if nose.y < avg_shoulder_y:
                status = True

        return [counter, status]

    def squat(self, counter, status):
        left_leg_angle = self.angle_of_the_left_leg()
        right_leg_angle = self.angle_of_the_right_leg()
        avg_leg_angle = (left_leg_angle + right_leg_angle) // 2

        if status:
            if avg_leg_angle < 70:
                counter += 1
                status = False
        else:
            if avg_leg_angle > 160:
                status = True

        return [counter, status]

    def walk(self, counter, status):
        right_knee = self.detection_body_part("RIGHT_KNEE")
        left_knee = self.detection_body_part("LEFT_KNEE")

        if status:
            if left_knee.x > right_knee.x:
                counter += 1
                status = False
        else:
            if left_knee.x < right_knee.x:
                counter += 1
                status = True

        return [counter, status]

    def sit_up(self, counter, status):
        angle = self.angle_of_the_abdomen()
        if status:
            if angle < 55:
                counter += 1
                status = False
        else:
            if angle > 105:
                status = True

        return [counter, status]
    def calculate_exercise(self, exercise_type, counter, status):
        if exercise_type == "leg_in_and_outs":
            counter, status = self.leg_in_and_outs(counter, status)
        elif exercise_type == "leg_lateral":
            counter, status = self.leg_lateral(counter, status)
        elif exercise_type == "push-up":
            counter, status = self.push_up(counter, status)
        elif exercise_type == "pull-up":
            counter, status = self.pull_up(counter, status)
        elif exercise_type == "squat":
            counter, status = self.squat(counter, status)
        elif exercise_type == "walk":
            counter, status = self.walk(counter, status)
        elif exercise_type == "sit-up":
            counter, status = self.sit_up(counter, status)

        return [counter, status]
