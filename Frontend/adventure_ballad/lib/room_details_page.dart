import 'package:flutter/material.dart';
import 'common_widgets.dart';
import 'loading_page.dart';

class RoomDetailsPage extends StatelessWidget {
  final String adventurerName;
  final String roomCode;
  final List<String> players;

  RoomDetailsPage({
    required this.adventurerName,
    required this.roomCode,
    required this.players,
  });

  void _startAdventure(BuildContext context) {
    if (players.length >= 2) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => LoadingPage(),
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('You need 4 players to start the adventure.'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Room Details'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Welcome, $adventurerName!',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 20),
            Text(
              'Room Code: $roomCode',
              style: TextStyle(fontSize: 18),
            ),
            SizedBox(height: 20),
            Text(
              'Players in Room:',
              style: TextStyle(fontSize: 18),
            ),
            SizedBox(height: 10),
            Column(
              children: players.map((player) => Text(player)).toList(),
            ),
            SizedBox(height: 30),
            fullWidthButton(
              text: 'Leave Room',
              onPressed: () {
                // Implement leave room functionality
              },
            ),
            SizedBox(height: 20),
            fullWidthButton(
              text: 'Start Adventure',
              onPressed: () => _startAdventure(context),
            ),
          ],
        ),
      ),
    );
  }
}
