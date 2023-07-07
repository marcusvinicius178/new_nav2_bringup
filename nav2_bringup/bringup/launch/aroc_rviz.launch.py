import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # Declare arguments
    model = LaunchConfiguration('model')
    rviz_config_file = LaunchConfiguration('rvizconfig')
    use_sim_time = LaunchConfiguration('use_sim_time', default='True')
    gui = LaunchConfiguration('gui', default='True')

    # Set default paths
    default_model_path = os.path.join(get_package_share_directory('nav2_bringup'), 'urdf', 'sam_bot.urdf')
    default_rviz_config_path = os.path.join(get_package_share_directory('nav2_bringup'), 'rviz', 'my_config.rviz')

    # Set Gazebo world file path
    world_path = os.path.join(get_package_share_directory('nav2_bringup'), 'worlds', 'empty_world.world')

    # Define Gazebo command
    gazebo_cmd = ['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so', world_path]

    return LaunchDescription([
        # Declare launch arguments
        DeclareLaunchArgument('gui', default_value='True', description='Flag to enable joint_state_publisher_gui'),
        DeclareLaunchArgument('model', default_value=default_model_path, description='Absolute path to robot urdf file'),
        DeclareLaunchArgument('rvizconfig', default_value=default_rviz_config_path, description='Absolute path to rviz config file'),
        DeclareLaunchArgument('use_sim_time', default_value='True', description='Flag to enable use_sim_time'),

        # Gazebo
        ExecuteProcess(cmd=gazebo_cmd, output='screen'),

        # Nodes
        Node(package='joint_state_publisher', executable='joint_state_publisher', output='screen', name='joint_state_publisher', parameters=[{'use_sim_time': use_sim_time}]),
        Node(package='robot_state_publisher', executable='robot_state_publisher', output='screen', name='robot_state_publisher', parameters=[{'robot_description': Command(['xacro ', model]), 'use_sim_time': use_sim_time}]),
        Node(package='gazebo_ros', executable='spawn_entity.py', arguments=['-entity', 'sam_bot', '-topic', 'robot_description'], output='screen'),
        Node(package='rviz2', executable='rviz2', output='screen', name='rviz2', arguments=['-d', rviz_config_file])
    ])
