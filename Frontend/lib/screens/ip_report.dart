import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class IpReport extends StatefulWidget {
  const IpReport({Key? key}) : super(key: key);

  @override
  IpReportState createState() => IpReportState();
}

class IpReportState extends State<IpReport> {
  final _ipController = TextEditingController();
  String _result = '';

  Future<void> _reportIp() async {
    String ip = _ipController.text.trim();
    String apiUrl = 'http://127.0.0.1:5000/report-ip'; // Adjusted endpoint for reporting IP

    try {
      final response = await http.post(Uri.parse(apiUrl),
          body: jsonEncode({'ip': ip}),
          headers: {'Content-Type': 'application/json'});

      if (response.statusCode == 200) {
        setState(() {
          _result = 'IP address $ip reported successfully!';
        });
      } else {
        try {
          final decodedResponse = jsonDecode(response.body);
          setState(() {
            _result = 'Error: ${decodedResponse['error']}';
          });
        } catch (e) {
          setState(() {
            _result = 'Error: Failed to parse error response';
          });
        }
      }
    } catch (e) {
      setState(() {
        _result = 'Error: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('IP Report'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const Text(
                'Enter an IP to report:',
                style: TextStyle(fontSize: 18),
              ),
              const SizedBox(height: 20),
              SizedBox(
                width: 300,
                child: TextField(
                  controller: _ipController,
                  decoration: const InputDecoration(
                    labelText: 'IP',
                    border: OutlineInputBorder(),
                  ),
                ),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _reportIp,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 20),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
                child: const Text(
                  'Report IP',
                  style: TextStyle(fontSize: 24),
                ),
              ),
              const SizedBox(height: 20),
              Container(
                width: 500,
                height: 100, // Adjust the height as needed
                padding: const EdgeInsets.all(8.0),
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Center(
                  child: Text(_result),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
