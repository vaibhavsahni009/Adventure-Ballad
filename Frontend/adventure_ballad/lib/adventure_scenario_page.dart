import 'package:flutter/material.dart';
import 'common_widgets.dart';
import 'story_page.dart';
import 'services/request_handler.dart'; // Make sure this import path is correct
import 'widgets/app_bar.dart';

class AdventureScenarioPage extends StatefulWidget {
  final String role;
  final String narration;
  final String roomCode;
  final String adventurerName;

  AdventureScenarioPage({
    required this.role,
    required this.narration,
    required this.roomCode,
    required this.adventurerName,
  });

  @override
  _AdventureScenarioPageState createState() => _AdventureScenarioPageState();
}

class _AdventureScenarioPageState extends State<AdventureScenarioPage> {
  final TextEditingController _responseController = TextEditingController();
  final RequestHandler _requestHandler = RequestHandler();

  Future<void> _submitResponse() async {
    final response = _responseController.text;
    if (response.isNotEmpty) {
      final body = {
        'code': widget.roomCode,
        'name': widget.adventurerName,
        'action': response,
      };

      try {
        final apiResponse = await _requestHandler.postRequest(
          'submit_action',
          body,
        );

        if (apiResponse.statusCode == 200) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Response submitted successfully'),
            ),
          );
          // Navigate to the next page or update the scenario
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => StoryPage(roomCode: widget.roomCode),
            ),
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Failed to submit response'),
            ),
          );
        }
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('An error occurred: $e'),
          ),
        );
      }
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Please enter a response'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        titleText: 'Adventurer Scenario',
        // No backgroundColor provided, so it will use the theme's primary color
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              'Role: ${widget.role}',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 20),
            Expanded(
              child: SingleChildScrollView(
                child: Text(
                  widget.narration,
                  style: TextStyle(fontSize: 18),
                ),
              ),
            ),
            SizedBox(height: 20),
            SizedBox(height: 20),
            customTextField(
                controller: _responseController, label: 'Enter your response'),
            SizedBox(height: 20),
            fullWidthButton(
              text: 'Submit Response',
              onPressed: _submitResponse,
            ),
          ],
        ),
      ),
    );
  }
}
