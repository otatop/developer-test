from lambdas.games import giantbomb_client
# TODO: Add integration tests for other modules & post deployment tests to run after the deploy. Consider tests in the
#  post hook in the template for blue/green deploys but weigh against additional complexity

def test_get_games():
    result = giantbomb_client.get_games(0)
    assert result["number_of_total_results"] > 1
    assert len(result["results"]) == 100
    assert result["results"][0]["api_detail_url"].startswith("https://www.giantbomb.com")