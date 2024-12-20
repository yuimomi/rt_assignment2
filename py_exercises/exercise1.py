# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


##Import ROS modules
import rclpy
from rclpy.node import Node

##Import ROS Messages and Services
from std_msgs.msg import String
from turtlesim.srv import Kill, Spawn
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        
        # initialize the client1
        self.cli1 = self.create_client(Kill, 'kill')
        # initialize self.req1
        self.req1 = Kill.Request()
        
        # initialize the client2
        self.cli2 = self.create_client(Spawn, 'spawn')
        # initialize self.req2
        self.req2 = Spawn.Request()
        
        #initialize publisher and subscriber
        self.subscription = self.create_subscription(
            Pose,
            'turtle2/pose',
            self.listener_callback,
            10
        )
        self.subscription

        self.publisher_ = self.create_publisher(Twist, 'turtle2/cmd_vel', 10)

        self.send_request()
        self.send_request2()
        
        while not self.cli1.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        
        while not self.cli2.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        
        
    def send_request(self):
        # set req1
        # call service 1
        self.req1.name = 'turtle1'
        future = self.cli1.call_async(self.req1)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.get_logger().info('Turtle1 killed successfully.')
        else:
            self.get_logger().error('Failed to kill Turtle1.')

        
    def send_request2(self):
        # set req2
        # call service2
        # Spawn a new turtle named turtle2 at given coordinates
        self.req2.x = 5.0
        self.req2.y = 5.0
        self.req2.theta = 0.0
        self.req2.name = 'turtle2'
        future = self.cli2.call_async(self.req2)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.get_logger().info(f'Successfully spawned {future.result().name}.')
        else:
            self.get_logger().error('Failed to spawn turtle2.')

        
    #publish a velocity message when something is received
    def listener_callback(self, msg):
        # When a pose message is received, publish a certain velocity
        vel_msg = Twist()
        # Example: move forward and turn a bit
        vel_msg.linear.x = 0.5
        vel_msg.angular.z = 0.5
        self.publisher_.publish(vel_msg)
        self.get_logger().info(f'Received pose: x={msg.x}, y={msg.y}, theta={msg.theta}')
        self.get_logger().info('Publishing velocity command.')
       


def main(args=None):
    #init the node
    rclpy.init(args=args)

    #call services 1 and 2
    minimal_subscriber = MinimalSubscriber()
    
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()