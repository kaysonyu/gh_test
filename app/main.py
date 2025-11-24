"""
简单的 Web 应用程序 Demo
用于演示 PR 分支测试
"""

import os
import sys
from datetime import datetime


class Application:
    def __init__(self):
        self.version = "1.0.0"
        self.branch = os.environ.get('PR_BRANCH', 'unknown')
        self.pr_number = os.environ.get('PR_NUMBER', 'N/A')
        self.environment = os.environ.get('ENVIRONMENT', 'development')

    def get_info(self):
        return {
            'version': self.version,
            'branch': self.branch,
            'pr_number': self.pr_number,
            'environment': self.environment,
            'timestamp': datetime.now().isoformat()
        }

    def run(self):
        print("=" * 60)
        print("Application Started")
        print("=" * 60)

        info = self.get_info()
        print(f"Version: {info['version']}")
        print(f"Branch: {info['branch']}")
        print(f"PR Number: {info['pr_number']}")
        print(f"Environment: {info['environment']}")
        print(f"Timestamp: {info['timestamp']}")
        print("=" * 60)

        return info

    def process_data(self, data):
        """处理数据的示例方法"""
        if not isinstance(data, (list, tuple)):
            raise ValueError("Data must be a list or tuple")

        return sum(data)

    def calculate(self, a, b):
        """简单的计算方法"""
        return a + b


def main():
    app = Application()
    info = app.run()

    # 示例计算
    result = app.calculate(10, 20)
    print(f"\nExample calculation: 10 + 20 = {result}")

    # 示例数据处理
    data = [1, 2, 3, 4, 5]
    total = app.process_data(data)
    print(f"Sum of {data} = {total}")

    print("\nApplication running successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
