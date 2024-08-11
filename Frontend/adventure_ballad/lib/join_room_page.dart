import 'dart:convert'; // Add this import
import 'package:flutter/material.dart';
import 'common_widgets.dart';
import 'room_details_page.dart';
import 'services/request_handler.dart';

class JoinRoomPage extends StatefulWidget {
  final String adventurerName;
  final RequestHandler requestHandler = RequestHandler();

  JoinRoomPage({required this.adventurerName});

  @override
  _JoinRoomPageState createState() => _JoinRoomPageState();
}

class _JoinRoomPageState extends State<JoinRoomPage> {
  final TextEditingController _roomCodeController = TextEditingController();

  Future<void> _joinRoom() async {
    final roomCode = _roomCodeController.text;
    if (roomCode.isNotEmpty) {
      try {
        final response = await widget.requestHandler.postRequest(
          '', // Replace with your actual endpoint path
          {
            'name': widget.adventurerName,
            'code': roomCode,
            'join': true,
          },
        );
        print(response);
        if (response.statusCode == 200) {
          // Decode the JSON response
          final responseData = jsonDecode(response.body);
          final roomCode = responseData['roomCode'];
          final players = List<String>.from(responseData['players']);

          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => RoomDetailsPage(
                adventurerName: widget.adventurerName,
                roomCode: roomCode,
                players: players,
              ),
            ),
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Failed to join the room. Please try again.'),
            ),
          );
        }
      } catch (e) {
        // Handle exceptions (e.g., network errors)
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('An error occurred: $e'),
          ),
        );
      }
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
              controller: _roomCodeController,
              label: 'Enter Room Code, ${widget.adventurerName}',
            ),
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
