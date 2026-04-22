import rclpy
from rclpy.node import Node
from mavros_msgs.msg import OverrideRCIn, State
from mavros_msgs.srv import CommandBool, SetMode
import time

class SquareMission(Node):
    def __init__(self):
        super().__init__('square_mission_node')
        self.rc_pub = self.create_publisher(OverrideRCIn, '/mavros/rc/override', 10)
        self.state_sub = self.create_subscription(State, '/mavros/state', self.state_cb, 10)
        self.arm_client = self.create_client(CommandBool, '/mavros/cmd/arming')
        self.mode_client = self.create_client(SetMode, '/mavros/set_mode')
        self.state = State()

        while rclpy.ok() and not self.state.connected:
            rclpy.spin_once(self)
            time.sleep(0.1)
        self.run_mission()

    def state_cb(self, msg):
        self.state = msg

    def send_cmd(self, fwd=1500, lat=1500, duration=3.0):
        msg = OverrideRCIn()
        # Fill with neutral (1500)
        msg.channels = [1500] * 18
        
        # In ArduSub Vectored:
        # Channel 5 is typically FORWARD
        # Channel 6 is typically LATERAL
        # We also set Channel 3 to 1500 to ensure we aren't "grounded"
        msg.channels[2] = 1500 # Throttle
        msg.channels[4] = fwd  # Forward
        msg.channels[5] = lat  # Lateral
        
        # If your frame is different, it might be using Ch 1/2 for Pitch/Roll
        # so we'll stick to 5 and 6 for now as they are the standard for BlueROV2.

        end_time = time.time() + duration
        while time.time() < end_time:
            self.rc_pub.publish(msg)
            # IMPORTANT: We need to keep the ROS node spinning to handle the serial heartbeat
            rclpy.spin_once(self, timeout_sec=0.05)
            time.sleep(0.1)

    def run_mission(self):
        # Force Mode
        self.mode_client.call_async(SetMode.Request(custom_mode='MANUAL'))
        time.sleep(1)

        # Persistent Arming
        self.get_logger().info("Attempting to Arm...")
        while not self.state.armed:
            self.arm_client.call_async(CommandBool.Request(value=True))
            rclpy.spin_once(self, timeout_sec=0.5)
            time.sleep(0.5)

        self.get_logger().info("ARMED! Starting Square.")

        # Side 1: Forward
        self.send_cmd(fwd=1800, duration=4.0)
        # Side 2: Right
        self.send_cmd(lat=1800, duration=4.0)
        # Side 3: Back
        self.send_cmd(fwd=1200, duration=4.0)
        # Side 4: Left
        self.send_cmd(lat=1200, duration=4.0)

        self.get_logger().info("Done.")
        self.arm_client.call_async(CommandBool.Request(value=False))

def main():
    rclpy.init()
    node = SquareMission()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
