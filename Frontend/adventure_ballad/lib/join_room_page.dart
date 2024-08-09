import 'package:flutter/material.dart';
import 'common_widgets.dart';
import 'room_details_page.dart';

class JoinRoomPage extends StatefulWidget {
  @override
  _JoinRoomPageState createState() => _JoinRoomPageState();
}

class _JoinRoomPageState extends State<JoinRoomPage> {
  final TextEditingController _roomCodeController = TextEditingController();

  void _joinRoom() {
    final roomCode = _roomCodeController.text;
    if (roomCode.isNotEmpty) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => RoomDetailsPage(), // Replace with actual page
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Please enter a room code'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Join Room'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            customTextField(
                controller: _roomCodeController, label: 'Enter Room Code'),
            SizedBox(height: 20),
            fullWidthButton(
              text: 'Join Room',
              onPressed: _joinRoom,
            ),
          ],
        ),
      ),
    );
  }
}
