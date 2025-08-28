using System.Net.Http.Json;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

record ForecastReq(int product_id,int store_id,int dow,int is_holiday,double price,double lag_1,double lag_7,double roll7);
record ForecastRes(double predicted_units);

var PYTHON_API = Environment.GetEnvironmentVariable("PYTHON_API_URL") ?? "http://localhost:8000";

app.MapPost("/api/forecast", async (ForecastReq req) =>
{
    using var http = new HttpClient { BaseAddress = new Uri(PYTHON_API) };
    var res = await http.PostAsJsonAsync("/forecast", req);
    if (!res.IsSuccessStatusCode)
    {
        return Results.Problem("Error from Python inference service", statusCode: 502);
    }
    var body = await res.Content.ReadFromJsonAsync<ForecastRes>();
    return Results.Ok(body);
});

app.Run();

