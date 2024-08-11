import 'package:flutter/material.dart';
import 'common_widgets.dart';
import 'story_page.dart';

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

  void _submitResponse() {
    final response = _responseController.text;
    if (response.isNotEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Response submitted: $response'),
        ),
      );
      // Navigate to the next page or update the scenario
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => StoryPage(),
        ),
      );
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
      appBar: AppBar(
        title: Text('Adventure Scenario'),
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
            Text(
              widget.narration,
              style: TextStyle(fontSize: 18),
            ),
            SizedBox(height: 20),
            Text(
              'Room Code: ${widget.roomCode}',
              style: TextStyle(fontSize: 16),
            ),
            SizedBox(height: 10),
            Text(
              'Adventurer Name: ${widget.adventurerName}',
              style: TextStyle(fontSize: 16),
            ),
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
