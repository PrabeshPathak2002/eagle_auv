import rclpy
from rclpy.node import Node
from mavros_msgs.srv import CommandBool, SetMode
from mavros_msgs.msg import State
import time

class DiveTest(Node):
    def __init__(self):
        super().__init__('dive_test_node')
        self.state = State()
        
        # Subscribe to state to check if we are ARMED and in the right MODE
        self.state_sub = self.create_subscription(State, '/mavros/state', self.state_cb, 10)
        
        self.arm_client = self.create_client(CommandBool, '/mavros/cmd/arming')
        self.mode_client = self.create_client(SetMode, '/mavros/set_mode')

        # Wait for MAVROS to actually connect to the Sub
        while rclpy.ok() and not self.state.connected:
            self.get_logger().info('Waiting for FCU connection...')
            rclpy.spin_once(self)
            time.sleep(0.5)

        self.run_mission()

    def state_cb(self, msg):
        self.state = msg

    def run_mission(self):
        # 1. Set Mode to ALT_HOLD (Depth Hold)
        self.get_logger().info('Changing to ALT_HOLD mode...')
        mode_req = SetMode.Request()
        mode_req.custom_mode = 'ALT_HOLD'
        
        future = self.mode_client.call_async(mode_req)
        rclpy.spin_until_future_complete(self, future)

        # 2. Arm the sub
        self.get_logger().info('Attempting to ARM...')
        arm_req = CommandBool.Request()
        arm_req.value = True
        
        future = self.arm_client.call_async(arm_req)
        rclpy.spin_until_future_complete(self, future)

        if self.state.armed:
            self.get_logger().info('SUB ARMED AND READY!')
        else:
            self.get_logger().error('ARMING FAILED - Check pre-arm failsafes')

def main(args=None):
    rclpy.init(args=args)
    node = DiveTest()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
