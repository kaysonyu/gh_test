"""
单元测试
"""

import sys
import os
import pytest

# 添加 app 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from main import Application


class TestApplication:
    def setup_method(self):
        """每个测试方法前执行"""
        self.app = Application()

    def test_application_info(self):
        """测试应用信息"""
        info = self.app.get_info()
        assert 'version' in info
        assert 'branch' in info
        assert 'pr_number' in info
        assert 'environment' in info
        assert 'timestamp' in info
        assert info['version'] == '1.0.0'

    def test_calculate(self):
        """测试计算功能"""
        assert self.app.calculate(10, 20) == 30
        assert self.app.calculate(0, 0) == 0
        assert self.app.calculate(-5, 5) == 0
        assert self.app.calculate(100, 200) == 300

    def test_process_data(self):
        """测试数据处理"""
        assert self.app.process_data([1, 2, 3]) == 6
        assert self.app.process_data([10, 20, 30]) == 60
        assert self.app.process_data([]) == 0

    def test_process_data_invalid_input(self):
        """测试无效输入"""
        with pytest.raises(ValueError):
            self.app.process_data("invalid")

        with pytest.raises(ValueError):
            self.app.process_data(123)

    def test_environment_variables(self):
        """测试环境变量"""
        # 设置环境变量
        os.environ['PR_BRANCH'] = 'feature/test'
        os.environ['PR_NUMBER'] = '123'

        app = Application()
        assert app.branch == 'feature/test'
        assert app.pr_number == '123'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
