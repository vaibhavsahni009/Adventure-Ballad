import 'dart:convert';
import 'package:http/http.dart' as http;

class RequestHandler {
  final String baseDomain = 'http://localhost:5000/';

  // GET request
  Future<http.Response> getRequest(String path,
      {Map<String, String>? headers}) async {
    final url = Uri.parse('$baseDomain$path');
    final response = await http.get(
      url,
      headers: headers,
    );

    _handleResponse(response);
    return response;
  }

  // POST request
  Future<http.Response> postRequest(String path, Map<String, dynamic> body,
      {Map<String, String>? headers}) async {
    final url = Uri.parse('$baseDomain$path');
    final response = await http.post(
      url,
      headers: headers ?? {'Content-Type': 'application/json'},
      body: jsonEncode(body),
    );

    _handleResponse(response);
    return response;
  }

  // Handle the response and errors
  void _handleResponse(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      // Request was successful
      print('Request successful: ${response.statusCode}');
    } else {
      // Request failed
      print('Request failed: ${response.statusCode}');
      throw Exception('Failed request: ${response.statusCode}');
    }
  }
}
