from locust import HttpUser, between, task, LoadTestShape


class WebsiteUser(HttpUser):
    host = "https://core.bomnet.shop"
    wait_time = between(1, 1)  # 1 ~ N 초에 한번 랜덤으로 요청
    # 고정 테스트::between(1, 1), 증가 테스트 between(1, 3)

    @task(3) #N 만큼의 비율로 요청
    def home_request(self):
        self.client.post(
            "/core/home",
            json={
                "device": "web",
                "endpoint": "test-endpoint",
                "p256dh": "fake-key-abc123==",
                "auth": "fake-auth-def456=="
            },
            headers={"Content-Type": "application/json"}
        )

    @task(2)
    def price_request(self):
        self.client.post(
            "/core/item/price",
            json={
                "item": "사과"
            },
            headers={"Content-Type": "application/json"}
        )


# ========== [ 고정 유저 테스트용 Shape 클래스 ] ==========
# 매 30초마다 100명씩 증가, 초당 100명 생성 → 2000명 도달까지 10분 소요
# 실행::locust -f locust.py --headless --html report_constant.html
class ConstantLoadShape(LoadTestShape):
    """
    ::고정 유저 테스트::
    30초마다 100명씩 증가, 최대 2000명까지
    초당 100명 생성
    """
    step_time = 30
    step_users = 100
    spawn_rate = 100
    max_users = 2000

    def tick(self):
        run_time = self.get_run_time()
        current_step = run_time // self.step_time
        user_count = min((current_step + 1) * self.step_users, self.max_users)

        if user_count > self.max_users:
            return None

        return (user_count, self.spawn_rate)


# ========== [ 점진적 증가 테스트용 Shape 클래스 ] ==========
# 매 60초마다 100명씩 증가, 초당 50명 생성
# 실행::locust -f locust.py --headless --html report_increment.html
# class IncrementalLoadShape(LoadTestShape):
#     """
#     ::점진적 증가 테스트::
#     60초마다 100명씩 증가, 최대 2000명까지
#     초당 50명 생성
#     """
#     step_time = 60
#     step_users = 100
#     spawn_rate = 50
#     max_users = 2000
#
#     def tick(self):
#         run_time = self.get_run_time()
#         current_step = run_time // self.step_time
#         user_count = min((current_step + 1) * self.step_users, self.max_users)
#
#         if user_count > self.max_users:
#             return None
#
#         return (user_count, self.spawn_rate)