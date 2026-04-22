import rclpy
from rclpy.node import Node
from eagle_interfaces.msg import Detection

class YoloNode(Node):
    def __init__(self):
        super().__init__('yolo_node')
        self.publisher_ = self.create_publisher(Detection, 'vision/gate_detection', 10)
        self.timer = self.create_timer(1.0, self.publish_detection)

    def publish_detection(self):
        msg = Detection()
        msg.label = "gate"
        msg.detected = True
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing detection...')

def main(args=None):
    rclpy.init(args=args)
    node = YoloNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()