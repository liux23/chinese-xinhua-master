# redis_countdown.py
import redis
import subprocess
import time
import atexit
import sys


class RedisManager:
    def __init__(self, server_path, conf_path):
        self.server_path = server_path
        self.conf_path = conf_path
        self.redis_process = None
        self.redis_client = None
        self.max_retries = 3

        # 注册退出时的清理
        atexit.register(self.stop_redis)

    def start_redis_server(self):
        """启动Redis服务器"""
        if self.redis_process is None:
            try:
                self.redis_process = subprocess.Popen(
                    [self.server_path, self.conf_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                time.sleep(2)  # 等待Redis启动
                print("Redis服务器已启动")
                return True
            except Exception as e:
                print(f"启动Redis服务器失败: {e}", file=sys.stderr)
                return False
        return True

    def connect_redis_client(self):
        """连接Redis客户端"""
        retries = 0
        while retries < self.max_retries:
            try:
                self.redis_client = redis.StrictRedis(
                    host='127.0.0.1',
                    port=6379,
                    db=0,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                    decode_responses=True
                )
                if self.redis_client.ping():
                    print("Redis客户端连接成功")
                    return True
            except redis.ConnectionError as e:
                print(f"Redis连接失败(尝试 {retries + 1}/{self.max_retries}): {e}")
                retries += 1
                time.sleep(1)
            except Exception as e:
                print(f"意外的Redis错误: {e}")
                break
        return False

    def ensure_connection(self):
        """确保Redis连接可用"""
        if self.redis_client is not None and self.redis_client.ping():
            return True

        return self.start_redis_server() and self.connect_redis_client()

    def stop_redis(self):
        """停止Redis服务"""
        if self.redis_client is not None:
            try:
                self.redis_client.close()
                print("Redis客户端连接已关闭")
            except Exception as e:
                print(f"关闭Redis客户端时出错: {e}")
            finally:
                self.redis_client = None

        if self.redis_process is not None:
            try:
                self.redis_process.terminate()
                self.redis_process.wait(timeout=5)
                print("Redis服务器已停止")
            except Exception as e:
                print(f"停止Redis服务器时出错: {e}")
            finally:
                self.redis_process = None

    def get_client(self):
        """获取Redis客户端实例"""
        if self.ensure_connection():
            return self.redis_client
        raise RuntimeError("无法获取Redis客户端连接")


# 配置Redis路径
REDIS_SERVER_PATH = r"D:\work software\redis\Redis\redis-server.exe"
REDIS_CONF_PATH = r"D:\work software\redis\Redis\redis.windows.conf"

# 创建全局Redis管理器实例
redis_manager = RedisManager(REDIS_SERVER_PATH, REDIS_CONF_PATH)