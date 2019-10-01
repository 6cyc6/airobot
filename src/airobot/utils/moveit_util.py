# modified from pyrobot.util
import rospy
import sys
from geometry_msgs.msg import PoseStamped
import moveit_commander
from moveit_commander import conversions


class MoveitScene(object):
    """
    Use this class to create objects that reside in moveit environments
    """

    def __init__(self):
        """
        Constructor of the MoveitObjectHandler class.
        """
        moveit_commander.roscpp_initialize(sys.argv)
        self.scene = moveit_commander.PlanningSceneInterface()
    def add_static_object(self, obj_name, pos, ori, size, ):
        pass

    
    def add_world_object_dp(self, id_name, pose, size, frame='/base'):
        '''
        Adds the particular object to the moveit planning scene

        :param id_name: unique id that object should be labeled with
        :param pose: pose of the object
        :param size: size of the object
        :param frame: frame in which the object pose is passed
        :type id_name: string
        :type pose: list of double of length 7 (x,y,z, q_x, q_y, q_z, q_w)
        :type size: tuple of length 3
        :type frame: string
        '''
        assert type(size) is tuple, 'size should be tuple'
        assert len(size) == 3, 'size should be of length 3'
        pose = conversions.list_to_pose(pose)
        pose_stamped = PoseStamped()
        pose_stamped.header.frame_id = frame
        pose_stamped.pose = pose
        self.scene.add_box(id_name, pose_stamped, size)
        rospy.sleep(1.0)
        self.scene.add_box(id_name, pose_stamped, size)

    def remove_world_object(self, id_name):
        '''
        Removes a specified object for the Moveit planning scene
        :param id_name: unique id that object should be labeled with
        :type frame: string
        '''
        self.scene.remove_world_object(id_name)
        self.scene.remove_world_object(id_name)

    def attach_arm_object(self, link_name, id_name, pose, size):
        '''
        Attaches the specified object to the robot
        :param link_name: name of the link to which the bject
                          should be attached
        :param id_name: unique id associated with the object
        :param pose: pose of the object
        :parma size: size of the object

        :type link_name: string
        :type id_name: string
        :type pose: list of double of length 7 (x,y,z, q_x, q_y, q_z, q_w)
        :type size: tuple of length 3
        '''
        assert type(size) is tuple, 'size should be tuple'
        assert len(size) == 3, 'size should be of length 3'
        pose = conversions.list_to_pose(pose)
        pose_stamped = PoseStamped()
        pose_stamped.header.frame_id = link_name
        pose_stamped.pose = pose
        self.scene.attach_box(link_name, id_name, pose_stamped, size)
        rospy.sleep(1.0)
        self.scene.attach_box(link_name, id_name, pose_stamped, size)

    def detach_arm_object(self, link_name, id_name, remove_from_world=True):
        '''
        Detaches an object earlier attached to the robot
        :param link_name: name of the link from which the bject
                          should be detached
        :param id_name: unique id associated with the object
        :param remove_from_world: if set true, deletes the
                                  object from the scene.

        :type link_name: string
        :type id_name: string
        :type remove_from_world: bool
        '''
        self.scene.remove_attached_object(link_name, id_name)
        self.scene.remove_attached_object(link_name, id_name)
        if remove_from_world is True:
            self.remove_world_object(id_name)

    def remove_all_objects(self):
        '''
        Removes all the objects in the current Moveit planning scene
        '''
        ## get add objects
        dict_obj = self.scene.get_objects()
        ## get attach object
        dict_attach_obj = self.scene.get_attached_objects()
        ## remove add objects
        for i in dict_obj.keys():
            self.remove_world_object(i)
        ## remove attached objects
        for i in dict_attach_obj.keys():
            self.detach_arm_object(dict_attach_obj[i].link_name, i)

    def add_table(self, pose=None, size=None):
        '''
        Adds a table in the planning scene in the base frame.

        :param pose: pose of the object
        :parma size: size of the object


        :type pose: list of double of length 7 (x,y,z, q_x, q_y, q_z, q_w)
        :type size: tuple of length 3
        '''
        if pose is not None and size is not None:
            self.add_world_object('table',
                                  pose=pose,
                                  size=size)
        else:
            # Default table.
            print('Creating default table.')
            self.add_world_object('table',
                                  pose=[0.8, 0.0, -0.23, 0., 0., 0., 1.],
                                  size=(1.35, 2.0, 0.1))

    def add_kinect(self, pose=None, size=None):
        '''
        Adds a kinect object to the planning scene in the base frame.
        :param pose: pose of the object
        :parma size: size of the object


        :type pose: list of double of length 7 (x,y,z, q_x, q_y, q_z, q_w)
        :type size: tuple of length 3
        '''
        if pose is not None and size is not None:
            self.add_world_object('kinect',
                                  pose=pose,
                                  size=size)
        else:
            # Default kinect.
            print('Creating default kinect.')
            self.add_world_object('kinect',
                                  pose=[0., 0.0, 0.75, 0., 0., 0., 1.],
                                  size=(0.25, 0.25, 0.3))

    def add_gripper(self, pose=None, size=None):
        '''
        Attaches gripper object to 'gripper' link.

        :param pose: pose of the object
        :parma size: size of the object


        :type pose: list of double of length 7 (x,y,z, q_x, q_y, q_z, q_w)
        :type size: tuple of length 3
        '''
        if pose is not None and size is not None:
            self.attach_arm_object('right_gripper',
                                   'gripper',
                                   pose=pose,
                                   size=size)
        else:
            # Default gripper.
            print('Creating default gripper.')
            self.attach_arm_object('right_gripper',
                                   'gripper',
                                   pose=[0., 0.0, 0.07, 0., 0., 0., 1.],
                                   size=(0.02, 0.1, 0.07))

    def remove_table(self):
        '''
        Removes table object from the planning scene
        '''
        self.remove_world_object('table')

    def remove_gripper(self):
        '''
        Removes table object from the planning scene
        '''
        self.detach_object('gripper')
        rospy.sleep(0.2)
        self.detach_object('gripper')
        rospy.sleep(0.2)
        self.remove_world_object('gripper')
        rospy.sleep(0.2)
        self.remove_world_object('gripper')