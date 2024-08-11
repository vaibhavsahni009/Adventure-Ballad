import 'dart:async';
import 'package:flutter/material.dart';
import 'package:adventure_ballad/adventure_scenario_page.dart';
import 'dart:convert';
import 'services/request_handler.dart';

class LoadingPage extends StatefulWidget {
  final String roomCode;
  final String adventurerName;

  LoadingPage({
    required this.roomCode,
    required this.adventurerName,
  });

  @override
  _LoadingPageState createState() => _LoadingPageState();
}

class _LoadingPageState extends State<LoadingPage> {
  late Timer _timer;
  bool _isPolling = false;
  final RequestHandler _requestHandler = RequestHandler();

  @override
  void initState() {
    super.initState();
    _startPolling();
  }

  void _startPolling() {
    _isPolling = true;
    _timer = Timer.periodic(Duration(seconds: 5), (timer) async {
      if (!_isPolling) {
        timer.cancel();
        return;
      }

      try {
        final response = await _requestHandler.getRequest(
            'fetch_scenario/${widget.roomCode}/${widget.adventurerName}');
        final data = jsonDecode(response.body);

        if (data['scenario_published'] == true) {
          // Scenario published, navigate to AdventureScenarioPage
          _isPolling = false;
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(
              builder: (context) => AdventureScenarioPage(
                role: data['role'] ??
                    'Unknown Role', // Default value if not found
                narration: data['text'] ??
                    'No narration available', // Default value if not found
                roomCode: widget.roomCode,
                adventurerName: widget.adventurerName,
              ),
            ),
          ).then((_) {
            // Ensure polling is stopped after navigating
            _isPolling = false;
            _timer.cancel();
          });
          timer.cancel();
        }
      } catch (e) {
        // Handle errors (e.g., network issues)
        print('Error during polling: $e');
        // Optionally stop polling on error
        _isPolling = false;
        timer.cancel();
      }
    });
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Loading'),
      ),
      body: Center(
        child: CircularProgressIndicator(),
      ),
    );
  }
}
