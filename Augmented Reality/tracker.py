import cv2 as cv
import numpy as np
import math
from random import *

class RANSAC:
    def __init__(self,prob_success=0.99,init_outlier_ratio=0.7,inlier_threshold=5.0):
        """ Initializes a RANSAC estimator.
            Arguments:
                prob_success: probability of success
                init_outlier_ratio: initial outlier ratio
                inlier_threshold: maximum re-projection error for inliers
        """
        self.prob_success=prob_success
        self.init_outlier_ratio=init_outlier_ratio
        self.inlier_threshold=inlier_threshold
    
    def compute_num_iter(self,outlier_ratio):
        """ Compute number of iterations given the current outlier ratio estimate.
            
            The number of iterations is computed as:
    
                N = ceil( log(1-p)/log(1-(1-e)^s) )
            
            where p is the probability of success,
                  e is the outlier ratio, and
                  s is the sample size.
    
            Arguments:
                outlier_ratio: current outlier ratio estimate
            Returns:
                number of iterations
        """
        s=4
        p=self.prob_success
        e=outlier_ratio
        return math.ceil((math.log(1-p))/(math.log(1-(1-e)**s)))
    
    def compute_inlier_mask(self,H,ref_pts,query_pts):
        """ Determine inliers given a homography estimate.
            
            A point correspondence is an inlier if its re-projection error is 
            below the given threshold.
            
            Arguments:
                H: homography to be applied to the reference points [3,3]
                ref_pts: reference points [N,1,2]
                query_pts: query points [N,1,2]
            Returns:
                Boolean array where mask[i] = True means the point i is an inlier. [N]
        """
        query_estimate = cv.perspectiveTransform(ref_pts,H)
        mask = []
        for i in range(len(query_estimate)):
            if np.linalg.norm(query_estimate[i] - query_pts[i]) <= self.inlier_threshold:
                mask.append(True)
            else:
                mask.append(False)
        return mask

    def find_homography(self,ref_pts,query_pts):
        """ Compute a homography and determine inliers using the RANSAC algorithm.
            
            The homography transforms the reference points to match the query points, i.e.
            
            query_pt ~ H * ref_pt
            
            Arguments:
                ref_pts: reference points [N,1,2]
                query_pts: query points [N,1,2]
            Returns:
                H: the computed homography estimate [3,3]
                mask: the Boolean inlier mask [N]
        """
        
        most_inliers = 0
        most_inlier_mask = None
        outlier_ratio = self.init_outlier_ratio
        
        ref_subset=[0,0,0,0]
        query_subset=[0,0,0,0]
        num_points = len(ref_pts)
        
        iter = 0
        while iter < self.compute_num_iter(outlier_ratio):
            #print(iter)
            iter+=1
            test_inlier = 0
            indexlist = sample(range(0, num_points), 4)
            for i in range(4):
                ref_subset[i]=ref_pts[indexlist[i]]
                query_subset[i]=query_pts[indexlist[i]]
            test_hom, _ = cv.findHomography(np.float32(ref_subset),np.float32(query_subset),method=0)
            test_mask = self.compute_inlier_mask(test_hom, ref_pts, query_pts)
            for bool in test_mask:
                if bool:
                    test_inlier+=1
            if test_inlier>=most_inliers:
                most_inliers=test_inlier
                most_inlier_mask=test_mask
                outlier_ratio = (num_points-most_inliers)/num_points
                iter=0
        
        final_ref_subset = []
        final_query_subset = []
        for i in range(num_points):
            if most_inlier_mask[i]:
                final_ref_subset.append(ref_pts[i])
                final_query_subset.append(query_pts[i])
        final_hom, _ = cv.findHomography(np.float32(final_ref_subset),np.float32(final_query_subset),method=0)
        final_mask = self.compute_inlier_mask(final_hom, ref_pts, query_pts)
        return final_hom, final_mask

class Tracker:
    def __init__(self,reference,overlay,min_match_count=10,inlier_threshold=5):
        """ Initializes a Tracker object.
            
            During initialization, this function will compute and store SIFT keypoints
            for the reference image.

            Arguments:
                reference: reference image
                overlay: overlay image for augmented reality effect
                min_match_count: minimum number of matches for a video frame to be processed.
                inlier_threshold: maximum re-projection error for inliers in homography computation
        """
        self.reference=reference
        self.overlay=overlay
        self.min_match_count=min_match_count
        self.inlier_threshold=inlier_threshold

        self.sift = cv.SIFT_create()
        self.bf_match = cv.BFMatcher()

        self.keypoints, self.descriptors = self.sift.detectAndCompute(self.reference,None)
        """img=cv.drawKeypoints(self.reference,self.keypoints,self.reference)
        cv.imshow('window',img)
        k = cv.waitKey(0)"""
        
    def compute_homography(self,frame,ratio_thresh=0.7):
        """ Calculate homography relating the reference image to a query frame.
            
            This function first finds matches between the query and reference
            by matching SIFT keypoints between the two image.  The matches are
            filtered using the ratio test.  A match is accepted if the first 
            nearest neighbor's distance is less than ratio_thresh * the second
            nearest neighbor's distance.
            
            RANSAC is then applied to matches that pass the ratio test, to determine
            inliers and compute a homography estimate.
            
            If less than min_match_count matches pass the ratio test,
            the function returns None.

            Arguments:
                frame: query frame from video
            Returns:
                the estimated homography [3,3] or None if not enough matches are found
        """
        img_keypoints, img_descriptors = self.sift.detectAndCompute(frame, None)
        matches = self.bf_match.knnMatch(self.descriptors,img_descriptors,k=2)
        good_matches = []
        #m1 is closest neighbor
        for m1, m2 in matches:
            if m1.distance<ratio_thresh*m2.distance:
                good_matches.append([m1])
        img = cv.drawMatchesKnn(self.reference,self.keypoints,frame,img_keypoints,good_matches,None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        """cv.imshow('window',img)
        k = cv.waitKey(0)"""
        if len(good_matches)<self.min_match_count:
            return None
        else:
            ref_kp = []
            frame_kp = []
            for match in good_matches:
                ref_index = match[0].queryIdx
                frame_index = match[0].trainIdx
                (x1,y1) = self.keypoints[ref_index].pt
                ref_kp.append((x1,y1))
                (x2,y2) = img_keypoints[frame_index].pt
                frame_kp.append((x2,y2))
            ransac = RANSAC()
            H, inliers = ransac.find_homography(np.float32(ref_kp).reshape(-1,1,2), np.float32(frame_kp).reshape(-1,1,2))
            #H, inliers = cv.findHomography(np.float32(ref_kp).reshape(-1,1,2), np.float32(frame_kp).reshape(-1,1,2), cv.RANSAC,self.inlier_threshold)
            return H
    
    def augment_frame(self,frame,H):
        """ Draw overlay image on video frame.
            
            Arguments:
                frame: frame to be drawn on [H,W,3]
                H: homography [3,3]
            Returns:
                augmented frame [H,W,3]
        """
        (oh,ow)=np.shape(self.overlay)[:2]
        (fh,fw)=np.shape(frame)[:2]
        
        corners = np.float32([[0,0], [0, oh-1], [ow-1,oh-1], [ow-1,0]]).reshape(-1,1,2)
        dst = cv.perspectiveTransform(corners, H).astype(np.int32)

        mask = np.ones((oh,ow,3))
        warped = cv.warpPerspective(self.overlay,H,(fw,fh))

        alpha = cv.warpPerspective(mask,H,(fw,fh))
        beta = (np.ones((fh,fw,3)))-alpha
        overlay = np.multiply(warped,alpha) + np.multiply(frame, beta)
        return cv.drawContours(overlay,[dst],-1, (255,127,0), 3).astype(np.uint8)

