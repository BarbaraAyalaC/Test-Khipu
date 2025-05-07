import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.StringJoiner;
import java.util.Base64;

public class CrearPagoKhipu {

    public static void main(String[] args) throws Exception {
        String receiverId = "Barbaraayalacastillo@gmail.com"; // Correito personal
        String secret = "8adfb5ba-82dd-4d4b-9517-3f457f10a711"; // Api generada
        String apiUrl = "https://khipu.com/api/2.0/payments";

        Map<String, String> params = Map.of(
            "receiver_id", receiverId,
            "subject", "Pago de prueba",
            "body", "Este es un pago generado de prueba",
            "amount", "5000",
            "currency", "CLP",
            "transaction_id", "orden-001",
            "payer_email", "cliente@correo.cl",
            "return_url", "https://tusitio.cl/retorno",
            "cancel_url", "https://tusitio.cl/cancelado",
            "notify_url", "https://tusitio.cl/notificacion"
        );

        StringJoiner sj = new StringJoiner("&");
        for (Map.Entry<String, String> entry : params.entrySet()) {
            sj.add(URLEncoder.encode(entry.getKey(), StandardCharsets.UTF_8) + "="
                    + URLEncoder.encode(entry.getValue(), StandardCharsets.UTF_8));
        }

        String auth = Base64.getEncoder().encodeToString((receiverId + ":" + secret).getBytes(StandardCharsets.UTF_8));

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(apiUrl))
                .header("Authorization", "Basic " + auth)
                .header("Content-Type", "application/x-www-form-urlencoded")
                .POST(HttpRequest.BodyPublishers.ofString(sj.toString()))
                .build();

        HttpClient client = HttpClient.newHttpClient();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        System.out.println("Respuesta de Khipu:");
        System.out.println(response.body());
    }
}
