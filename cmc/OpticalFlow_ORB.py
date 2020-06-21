import cv2
import numpy as np
import argparse
from matplotlib import pyplot as plt


class OpticalFlow_ORB(object):
    def __init__(self, video_frames=None):
        #self.video_name = "C:\\Users\\dhelm\\Documents\\slow_traffic_small.mp4"
        #self.video_name = "C:\\Users\\dhelm\\Documents\\training_data_patrick_link\\training_data\\tilt\\b88f0e71-a0f2-4efe-ae0d-5b83a0770b73_32.mp4"  # tilt unten nach oben
        #self.video_name = "C:\\Users\\dhelm\\Documents\\training_data_patrick_link\\training_data\\tilt\\35_25178.mp4"  # tilt oben nach unten
        #self.video_name = "C:\\Users\\dhelm\\Documents\\training_data_patrick_link\\training_data\\tilt\\94_24357.mp4" # tilt unten nach oben
        #1371a561-6b19-4d69-8210-1347ca75eb90_96
        # self.video_name = "C:\\Users\\dhelm\\Documents\\training_data_patrick_link\\training_data\\pan\\1371a561-6b19-4d69-8210-1347ca75eb90_104.mp4"
        # self.video_name = "C:\\Users\\dhelm\\Documents\\training_data_patrick_link\\training_data\\tilt\\tilt_130_74088.mp4"
        #self.video_name = "C:\\Users\\dhelm\\Documents\\training_data_patrick_link\\training_data\\pan\\130_74173.mp4"
        #self.video_name = "C:\\Users\\dhelm\\Documents\\training_data_patrick_link\\training_data\\pan\\1371a561-6b19-4d69-8210-1347ca75eb90_96.mp4"
        #self.video_name = "C:\\Users\\dhelm\\Documents\\training_data_patrick_link\\training_data\\pan\\066f929d-6434-4ea9-844b-e066f57b6c28_99.mp4" # rechts nach links
        #self.video_name = "C:\\Users\\dhelm\\Documents\\999.mp4"
        #self.video_name = "C:\\Users\\dhelm\\Documents\\444.mp4"
        #self.video_name = "C:\\Users\\dhelm\\Documents\\training_data_patrick_link\\training_data\\pan\\72_65942.mp4"  # pan links nach rechts

        self.video_frames = video_frames

    def run(self):

        '''
        frame_list = []
        cap = cv2.VideoCapture(self.video_name)
        while(1):
            ret, old_frame = cap.read()
            if(ret == False):
                break
            old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
            old_gray = self.crop(old_gray, (500, 500))
            frame_list.append(old_gray)
        frames_np = np.array(frame_list)
        print(frames_np.shape)
        cap.release()
        '''

        frames_np = self.video_frames

        REQUIRED_FEATURES = 500
        angles_l = []
        angles_l_n = []
        mag_l = []
        for i in range(1, len(frames_np)):
            print("##########")
            kp_prev_list, kp_curr_list = self.getORBMatches(frames_np[i - 1], frames_np[i])
            print(len(kp_curr_list))
            print(len(kp_prev_list))

            if(len(kp_prev_list) == 0 or len(kp_curr_list) == 0):
                continue

            #kp_prev_list, kp_curr_list = self.getORBMatches(frames_np[i-1], frames_np[i])
            #kp_prev_list, kp_curr_list = [[100,100]], [[50,50]]

            curr_points = np.array(kp_curr_list).astype('float').reshape(-1, 1, 2)
            prev_points = np.array(kp_prev_list).astype('float').reshape(-1, 1, 2)
            mag_n, angle_n = self.compute_magnitude_angle(prev_points,
                                                          curr_points)
            #print(mag_n.shape)
            #print(angle_n.shape)

            mag_mean_n = np.mean(mag_n)
            # angle_mean_n = np.mean(angle_n)

            angle_n = np.abs(angle_n) #[:50])
            #print(angle_n)



            angle_mean_n = np.mean(angle_n)
            angles_l_n.append(angle_mean_n)

            #exit()

            #print(kp_prev_list[:50])
            #print(kp_curr_list[:50])
            #print(mag_n)
            #print(angle_n)
            #print(mag_mean_n)
            #print(angle_mean_n)
            #print(len(kp_prev_list))

            '''
            # draw the tracks
            mask = np.zeros_like(frames_np[i])
            for j, (new, old) in enumerate(zip(curr_points, prev_points)):
                if(j > 10):
                    break;
                a, b = new.ravel().astype('int')
                c, d = old.ravel().astype('int')
                mask = cv2.line(mask, (a, b), (c, d), (255, 0, 0), 1)
                frame_curr = cv2.circle(frames_np[i], (a, b), 5, (255, 0, 0), -1)
            img = cv2.add(frame_curr, mask)
            cv2.imshow('frame', img)
            '''

            '''
            # draw orig with n feature points
            n_feature_points = 15
            for j, (new, old) in enumerate(zip(curr_points, prev_points)):
                if(j > n_feature_points):
                    break
                a, b = new.astype('int').ravel()
                c, d = old.astype('int').ravel()
                frame_curr = cv2.circle(frames_np[i], (a, b), 5, (255, 0, 0), -1)
            #img = cv2.add(frame_curr, mask)
            cv2.imshow('frame', frame_curr)
            '''

            '''
            # draw original
            #img = cv2.add(frames_np[i], mask)
            cv2.imshow('frame', frames_np[i])
            '''

            '''
            # plot angles over time
            plt.figure(1)
            plt.plot(np.arange(len(angles_l_n)), angles_l_n)
            # plt.plot(np.arange(len(mag_l)), mag_l)
            plt.ylim(ymax=190, ymin=-190)
            plt.grid(True)
            # plt.show()
            plt.draw()
            plt.pause(0.002)
            ''''''
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
            '''


            '''
            result1 = frames_np[i-1].copy()
            for s in range(0, len(kp_prev_list)):
                #result = cv2.circle(result, (int(kp_curr_list[0][0]), int(kp_curr_list[0][1])), radius=0, color=(0, 0, 255), thickness=-1)
                result1 = cv2.circle(result1, (int(kp_prev_list[0][0]), int(kp_prev_list[0][1])), radius=5, color=(255, 0, 0),
                                    thickness=5)
            print(result1.shape)

            result2 = frames_np[i].copy()
            for s in range(0, len(kp_curr_list)):
                # result = cv2.circle(result, (int(kp_curr_list[0][0]), int(kp_curr_list[0][1])), radius=0, color=(0, 0, 255), thickness=-1)
                result2 = cv2.circle(result2, (int(kp_curr_list[0][0]), int(kp_curr_list[0][1])), radius=4,
                                     color=(255, 0, 0),
                                     thickness=5)
            print(result2.shape)
            
            result = np.concatenate((result1, result2), axis=1)
            
            # Display the best matching points
            plt.figure(2)
            plt.title('Best Matching Points')
            plt.imshow(result)
            plt.draw()
            plt.pause(0.005)
            '''
        return angles_l_n

    def predict_final_result(self, angles_l_n):
        # calcualate final result

        print(np.mean(angles_l_n))
        angles_np = np.array(angles_l_n)
        print(np.mean(angles_np))

        return np.mean(angles_np)

    def getORBMatches(self, frame1, frame2):
        kp_curr_list = []
        kp_prev_list = []

        orb = cv2.ORB_create()
        kp_prev, descriptor_prev = orb.detectAndCompute(frame1, None)
        kp_curr, descriptor_curr = orb.detectAndCompute(frame2, None)


        #print(descriptor_prev)
        #print(descriptor_curr)

        print(type(descriptor_prev))
        print(type(descriptor_curr))

        out_frame1 = frame1.copy()
        #img = cv2.drawKeypoints(old_frame, kp, out_img)
        #out_img_prev = cv2.drawKeypoints(frames_np[i-1],
        #                                 kp_prev,
        #                                 out_img_prev,
        #                                 flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        out_frame2 = frame2.copy()
        # img = cv2.drawKeypoints(old_frame, kp, out_img)
        #out_img_curr = cv2.drawKeypoints(frames_np[i - 1],
        #                                 kp_curr,
        #                                 out_img_curr,
        #                                 flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        #print(out_img_prev.shape)
        #print(out_img_curr.shape)

        # Create a Brute Force Matcher object.
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # Perform the matching between the ORB descriptors of the training image and the test image
        try:
            matches = bf.match(descriptor_prev, descriptor_curr)
        except:
            return kp_prev_list, kp_curr_list

        #print(matches)
        print(type(matches))
        if (len(matches) == 0):
            return kp_prev_list, kp_curr_list

        print(descriptor_prev.shape)
        #matches = bf.knnMatch(descriptor_prev, descriptor_curr, k=3)

        # The matches with shorter distance are the ones we want.
        matches = sorted(matches, key=lambda x: x.distance)

        for match in matches:
            kp_curr_list.append(kp_curr[match.trainIdx].pt)
            kp_prev_list.append(kp_prev[match.queryIdx].pt)

        '''
        result = cv2.drawMatches(out_img_curr, kp_curr, out_img_prev, kp_prev, matches[:1], out_img_prev, flags=2)
        # Display the best matching points
        plt.title('Best Matching Points')
        plt.imshow(result)
        plt.draw()
        plt.pause(0.05)
        '''
        return kp_prev_list, kp_curr_list

    def crop(self, img: np.ndarray, dim: tuple):
        """
        This method is used to crop a specified region of interest from a given image.

        :param img: This parameter must hold a valid numpy image.
        :param dim: This parameter must hold a valid tuple including the crop dimensions.
        :return: This method returns the cropped image.
        """
        crop_w, crop_h = dim

        crop_h_1 = 0
        crop_h_2 = 0
        crop_w_1 = 0
        crop_w_2 = 0

        img_h = img.shape[0]
        img_w = img.shape[1]

        crop_w_1 = int(img_w / 2) - int(crop_w / 2)
        if (crop_w_1 < 0):
            crop_w_1 = 0

        crop_w_2 = int(img_w / 2) + int(crop_w / 2)
        if (crop_w_2 >= img_w):
            crop_w_2 = img_w

        crop_h_1 = int(img_h / 2) - int(crop_h / 2)
        if (crop_h_1 < 0):
            crop_h_1 = 0

        crop_h_2 = int(img_h / 2) + int(crop_h / 2)
        if (crop_h_2 >= img_h):
            crop_h_2 = img_h

        img_crop = img[crop_h_1:crop_h_2, crop_w_1:crop_w_2]
        return img_crop

    def compute_magnitude_angle(self, prev_feat, curr_feat):
        if prev_feat.__len__() <= 0:
            print("no previous features... returning")
            assert (prev_feat.__len__() > 0)
        if prev_feat.__len__() != curr_feat.__len__():
            print("length is not correct")
            assert (prev_feat.__len__() == curr_feat.__len__())
        d = curr_feat - prev_feat
        print(d.shape)
        mag = np.hypot(d[:, 0, 0], d[:, 0, 1])
        ang = np.round(np.degrees(np.arctan2(d[:, 0, 1], d[:, 0, 0])))

        #ang = np.round(np.arctan2(d[:, 0, 1], d[:, 0, 0])*180 / np.pi)

        return mag, ang

