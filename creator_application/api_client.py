import httpx


class CVApiClient:
    def __init__(self, base_url: str, timeout: float = 60.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate_cv(self, payload: dict) -> dict:
        url = f"{self.base_url}/cv_generate/generate"

        response = httpx.post(
            url,
            json=payload,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()


    def populate_candidate(self, payload: dict) -> dict:
        url = f"{self.base_url}/populate_db/candidate"

        response = httpx.post(
            url,
            json=payload,
            timeout=60.0,
        )

        response.raise_for_status()

        return response.json()

    
    def get_candidates(self):
        url = f"{self.base_url}/cv_generate/candidates"
        candidates = httpx.get(
            url,
            timeout=60.0,
        )
        return candidates.json()