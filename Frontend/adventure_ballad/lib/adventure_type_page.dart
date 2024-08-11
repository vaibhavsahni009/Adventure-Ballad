import 'dart:convert'; // Add this import
import 'package:flutter/material.dart';
import 'common_widgets.dart';
import 'room_details_page.dart';
import 'services/request_handler.dart';

class AdventureTypePage extends StatelessWidget {
  final String adventurerName;
  final RequestHandler requestHandler = RequestHandler();

  AdventureTypePage({required this.adventurerName});

  Future<void> _selectAdventure(
      BuildContext context, String adventureType) async {
    try {
      final response = await requestHandler.postRequest(
        '', // Replace with your actual endpoint path
        {
          'name': adventurerName,
          'code': adventureType,
          'create': true,
        },
      );

      print(response);
      print(jsonDecode(response.body));

      if (response.statusCode == 200) {
        // Decode the JSON response
        final responseData = jsonDecode(response.body);
        final roomCode = responseData['roomCode'];
        final players = List<String>.from(responseData['players']);

        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => RoomDetailsPage(
              adventurerName: adventurerName,
              roomCode: roomCode,
              players: players,
            ),
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to start the adventure. Please try again.'),
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
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Choose Your Adventure'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            fullWidthButton(
              text: 'Pirate',
              onPressed: () => _selectAdventure(context, 'Pirate'),
            ),
            SizedBox(height: 20),
            fullWidthButton(
              text: 'Medieval',
              onPressed: () => _selectAdventure(context, 'Medieval'),
            ),
            SizedBox(height: 20),
            fullWidthButton(
              text: 'Sci-Fi',
              onPressed: () => _selectAdventure(context, 'Sci-Fi'),
            ),
            SizedBox(height: 20),
            fullWidthButton(
              text: 'Fantasy',
              onPressed: () => _selectAdventure(context, 'Fantasy'),
            ),
          ],
        ),
      ),
    );
  }
}
