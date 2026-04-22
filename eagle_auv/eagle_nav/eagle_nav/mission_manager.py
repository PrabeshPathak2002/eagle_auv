import rclpy
from .sub_pilot import SubPilot
from eagle_interfaces.msg import Detection
import time

class MissionManager(SubPilot):
    def __init__(self):
        super().__init__('mission_manager')
        
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        # Subscribe to the vision topic
        self.vision_sub = self.create_subscription(
            Detection,
            '/vision/gate_detection',
            self.vision_callback,
            10)
        self.latest_detection = None
    
    def move_sub(self, linear_x=0.0, linear_y=0.0, linear_z=0.0, angular_z=0.0):
        """Sends velocity commands to the Gazebo simulation (or real sub)."""
        msg = Twist()
        msg.linear.x = float(linear_x)
        msg.linear.y = float(linear_y)
        msg.linear.z = float(linear_z)
        
        # We usually ignore roll and pitch for basic navigation
        msg.angular.x = 0.0 
        msg.angular.y = 0.0
        msg.angular.z = float(angular_z)
        
        self.cmd_vel_pub.publish(msg)
        self.get_logger().info(f'Moving -> Surge: {linear_x}, Sway: {linear_y}, Depth: {linear_z}, Yaw: {angular_z}')

    def vision_callback(self, msg):
        self.latest_detection = msg
        if msg.detected:
            # Example Logic: If the gate is to the right (positive X offset), strafe right.
            if msg.x_offset > 0.1:
                self.move_sub(linear_y=-0.5) # Strafe right
            elif msg.x_offset < -0.1:
                self.move_sub(linear_y=0.5)  # Strafe left
            else:
                self.move_sub(linear_x=0.5)  # Drive forward through the gate

    def start_mission(self):
        self.get_logger().info("EagleAUV: Searching for gate...")
        # Now you can add logic like:
        # if self.latest_detection and self.latest_detection.detected:
        #     self.align_with_gate()

def main():
    rclpy.init()
    node = MissionManager()
    node.start_mission()
    
    try:
    	rclpy.spin(node)
    except KeyboardInterrupt:
    	pass
    	
    node.destroy_node()
    rclpy.shutdown()
