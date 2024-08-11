import 'package:flutter/material.dart';
import 'adventure_type_page.dart';
import 'common_widgets.dart';
import 'join_room_page.dart';

class GreetingPage extends StatelessWidget {
  final String adventurerName;

  GreetingPage({required this.adventurerName});

  void _navigateToAdventureType(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => AdventureTypePage(adventurerName: adventurerName),
      ),
    );
  }

  void _navigateToJoinRoom(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => JoinRoomPage(adventurerName: adventurerName),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Hello, Adventurer!'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Hello, Adventurer $adventurerName!',
              style: TextStyle(fontSize: 24),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 40),
            fullWidthButton(
              text: 'Create Room',
              onPressed: () => _navigateToAdventureType(context),
            ),
            SizedBox(height: 40),
            fullWidthButton(
              text: 'Join Room',
              onPressed: () => _navigateToJoinRoom(context),
            ),
          ],
        ),
      ),
    );
  }
}
