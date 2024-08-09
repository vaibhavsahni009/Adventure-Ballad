import 'package:adventure_ballad/final_page.dart';
import 'package:flutter/material.dart';

import 'common_widgets.dart';

class StoryPage extends StatelessWidget {
  final String story =
      'The full story of the adventure goes here...'; // Example story

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Adventure Story'),
      ),
      body: Column(
        children: [
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: SingleChildScrollView(
                child: Text(
                  story,
                  style: TextStyle(fontSize: 18),
                ),
              ),
            ),
          ),
          SizedBox(height: 20),
          fullWidthButton(
            text: 'Start Adventure',
            onPressed: () {
              // Implement start adventure functionality
              _goToSongPage(context);
            },
          ),
        ],
      ),
    );
  }

  void _goToSongPage(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => FinalPage(),
      ),
    );
  }
}
