import rclpy
from rclpy.node import Node
from mavros_msgs.msg import OverrideRCIn, State
from mavros_msgs.srv import CommandBool, SetMode

class SubPilot(Node):
    def __init__(self, node_name='sub_pilot'):
        super().__init__(node_name)
        
        # Internal State
        self.current_state = State()
        
        # MAVROS Communication
        self.state_sub = self.create_subscription(State, '/mavros/state', self._state_cb, 10)
        self.rc_pub = self.create_publisher(OverrideRCIn, '/mavros/rc/override', 10)
        
        self.arm_client = self.create_client(CommandBool, '/mavros/cmd/arming')
        self.mode_client = self.create_client(SetMode, '/mavros/set_mode')

    def _state_cb(self, msg):
        self.current_state = msg

    def set_mode(self, mode_name):
        self.get_logger().info(f"Changing to {mode_name} mode...")
        req = SetMode.Request(custom_mode=mode_name)
        return self.mode_client.call_async(req)

    def arm(self, value=True):
        self.get_logger().info("Arming..." if value else "Disarming...")
        req = CommandBool.Request(value=value)
        return self.arm_client.call_async(req)

    def send_controls(self, fwd=1500, lat=1500, thr=1500, yaw=1500):
        """Standardizes movement commands."""
        msg = OverrideRCIn()
        msg.channels = [1500] * 18
        msg.channels[2] = int(thr) #vertical
        msg.channels[3] = int(yaw)      #rotation
        msg.channels[4] = int(fwd)  #pitch
        msg.channels[5] = int(lat)  #roll
        self.rc_pub.publish(msg)
