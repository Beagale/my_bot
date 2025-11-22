# FIX 1: MIGHT NEED TO ADJUST URDF FILE FOR THIS (READ CHAT THREAD)
# import os

# from ament_index_python.packages import get_package_share_directory


# from launch import LaunchDescription
# from launch.actions import IncludeLaunchDescription, TimerAction
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from launch.substitutions import Command
# from launch.actions import RegisterEventHandler
# from launch.event_handlers import OnProcessStart

# from launch_ros.actions import Node

# # ADDED FOR NEW WAY TO GET robot_description
# from launch_ros.substitutions import FindPackageShare
# from launch.substitutions import PathJoinSubstitution, Command



# def generate_launch_description():


#     # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
#     # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

#     package_name='my_bot' #<--- CHANGE ME

#     rsp = IncludeLaunchDescription(
#                 PythonLaunchDescriptionSource([os.path.join(
#                     get_package_share_directory(package_name),'launch','rsp.launch.py'
#                 )]), launch_arguments={'use_sim_time': 'false', 'use_ros2_control': 'true'}.items()
#     )

#     # joystick = IncludeLaunchDescription(
#     #             PythonLaunchDescriptionSource([os.path.join(
#     #                 get_package_share_directory(package_name),'launch','joystick.launch.py'
#     #             )])
#     # )


#     twist_mux_params = os.path.join(get_package_share_directory(package_name),'config','twist_mux.yaml')
#     twist_mux = Node(
#             package="twist_mux",
#             executable="twist_mux",
#             parameters=[twist_mux_params],
#             remappings=[('/cmd_vel_out','/diff_cont/cmd_vel_unstamped')]
#         )

    

#     # GET robot_description FROM .xacro FILE INSTEAD OF RUNNING ANOTHER PROCESS
#     # robot_description = Command(['ros2 param get --hide-type /robot_state_publisher robot_description'])
#     robot_description = Command([
#         'xacro ',
#         PathJoinSubstitution([
#             FindPackageShare(package_name),
#             'description',#'urdf',
#             'robot_core.xacro'
#         ])
#     ])

#     controller_params_file = os.path.join(get_package_share_directory(package_name),'config','my_controllers.yaml')

#     controller_manager = Node(
#         package="controller_manager",
#         executable="ros2_control_node",
#         parameters=[{'robot_description': robot_description},
#                     controller_params_file]
#     )

#     delayed_controller_manager = TimerAction(period=3.0, actions=[controller_manager])

#     diff_drive_spawner = Node(
#         package="controller_manager",
#         executable="spawner.py",
#         arguments=["diff_cont"],
#     )

#     delayed_diff_drive_spawner = RegisterEventHandler(
#         event_handler=OnProcessStart(
#             target_action=controller_manager,
#             on_start=[diff_drive_spawner],
#         )
#     )

#     joint_broad_spawner = Node(
#         package="controller_manager",
#         executable="spawner.py",
#         arguments=["joint_broad"],
#     )

#     delayed_joint_broad_spawner = RegisterEventHandler(
#         event_handler=OnProcessStart(
#             target_action=controller_manager,
#             on_start=[joint_broad_spawner],
#         )
#     )


#     # Code for delaying a node (I haven't tested how effective it is)
#     # 
#     # First add the below lines to imports
#     # from launch.actions import RegisterEventHandler
#     # from launch.event_handlers import OnProcessExit
#     #
#     # Then add the following below the current diff_drive_spawner
#     # delayed_diff_drive_spawner = RegisterEventHandler(
#     #     event_handler=OnProcessExit(
#     #         target_action=spawn_entity,
#     #         on_exit=[diff_drive_spawner],
#     #     )
#     # )
#     #
#     # Replace the diff_drive_spawner in the final return with delayed_diff_drive_spawner



#     # Launch them all!
#     return LaunchDescription([
#         rsp,
#         # joystick,
#         twist_mux,
#         delayed_controller_manager,
#         delayed_diff_drive_spawner,
#         delayed_joint_broad_spawner
#     ])

# # FIX 1b (USE ASYNCHRONOUS, REFER TO CHAT)
# import os

# from ament_index_python.packages import get_package_share_directory

# from launch import LaunchDescription, TimerAction
# from launch.actions import IncludeLaunchDescription, RegisterEventHandler
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from launch.substitutions import Command, PathJoinSubstitution
# from launch.event_handlers import OnProcessStart
# from launch_ros.actions import Node
# from launch_ros.substitutions import FindPackageShare


# def generate_launch_description():

#     package_name = 'my_bot'  # <-- CHANGE ME if needed

#     # Include robot_state_publisher launch
#     rsp = IncludeLaunchDescription(
#         PythonLaunchDescriptionSource([os.path.join(
#             get_package_share_directory(package_name), 'launch', 'rsp.launch.py'
#         )]),
#         launch_arguments={'use_sim_time': 'false', 'use_ros2_control': 'true'}.items()
#     )

#     # Twist mux node
#     twist_mux_params = os.path.join(get_package_share_directory(package_name), 'config', 'twist_mux.yaml')
#     twist_mux = Node(
#         package="twist_mux",
#         executable="twist_mux",
#         parameters=[twist_mux_params],
#         remappings=[('/cmd_vel_out', '/diff_cont/cmd_vel_unstamped')]
#     )

#     # Robot description from robot_state_publisher (could also switch to xacro here)
#     robot_description = Command([
#         'ros2 param get --hide-type /robot_state_publisher robot_description'
#     ])

#     # Controller manager node
#     controller_params_file = os.path.join(get_package_share_directory(package_name), 'config', 'my_controllers.yaml')
#     controller_manager = Node(
#         package="controller_manager",
#         executable="ros2_control_node",
#         parameters=[{'robot_description': robot_description}, controller_params_file],
#         output='screen'
#     )

#     # Diff drive controller spawner (will run AFTER controller_manager starts)
#     diff_drive_spawner = Node(
#         package="controller_manager",
#         executable="spawner.py",
#         arguments=["diff_cont"],
#         output='screen'
#     )

#     joint_broad_spawner = Node(
#         package="controller_manager",
#         executable="spawner.py",
#         arguments=["joint_broad"],
#         output='screen'
#     )

#     # Register event handler: spawn controllers AFTER controller_manager starts
#     delayed_controller_spawners = RegisterEventHandler(
#         OnProcessStart(
#             target_action=controller_manager,
#             on_start=[
#                 TimerAction(
#                     period=1.0,  # optional small delay to be safe
#                     actions=[diff_drive_spawner, joint_broad_spawner]
#                 )
#             ]
#         )
#     )

#     # Launch all nodes
#     return LaunchDescription([
#         rsp,
#         twist_mux,
#         controller_manager,
#         delayed_controller_spawners
#     ])


# ORIGINAL w/ INCREASED TIME DELAY
import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart

from launch_ros.actions import Node



def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='my_bot' #<--- CHANGE ME

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'false', 'use_ros2_control': 'true'}.items()
    )

    # joystick = IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource([os.path.join(
    #                 get_package_share_directory(package_name),'launch','joystick.launch.py'
    #             )])
    # )


    twist_mux_params = os.path.join(get_package_share_directory(package_name),'config','twist_mux.yaml')
    twist_mux = Node(
            package="twist_mux",
            executable="twist_mux",
            parameters=[twist_mux_params],
            remappings=[('/cmd_vel_out','/diff_cont/cmd_vel_unstamped')]
        )

    


    robot_description = Command(['ros2 param get --hide-type /robot_state_publisher robot_description'])

    controller_params_file = os.path.join(get_package_share_directory(package_name),'config','my_controllers.yaml')

    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[{'robot_description': robot_description},
                    controller_params_file]
    )

    delayed_controller_manager = TimerAction(period=8.0, actions=[controller_manager]) # fix 2 had 5.5 s

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["diff_cont"],
    )

    delayed_diff_drive_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[diff_drive_spawner],
        )
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["joint_broad"],
    )

    delayed_joint_broad_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[joint_broad_spawner],
        )
    )


    # Code for delaying a node (I haven't tested how effective it is)
    # 
    # First add the below lines to imports
    # from launch.actions import RegisterEventHandler
    # from launch.event_handlers import OnProcessExit
    #
    # Then add the following below the current diff_drive_spawner
    # delayed_diff_drive_spawner = RegisterEventHandler(
    #     event_handler=OnProcessExit(
    #         target_action=spawn_entity,
    #         on_exit=[diff_drive_spawner],
    #     )
    # )
    #
    # Replace the diff_drive_spawner in the final return with delayed_diff_drive_spawner



    # Launch them all!
    return LaunchDescription([
        rsp,
        # joystick,
        twist_mux,
        delayed_controller_manager,
        delayed_diff_drive_spawner,
        delayed_joint_broad_spawner
    ])