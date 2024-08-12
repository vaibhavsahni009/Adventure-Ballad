import 'dart:convert'; // Add this import
import 'package:flutter/material.dart';
import 'common_widgets.dart';
import 'room_details_page.dart';
import 'services/request_handler.dart';
import 'widgets/app_bar.dart';

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
          'adventure_type': adventureType,
          'create': true,
        },
      );

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
      appBar: CustomAppBar(
        titleText: 'Choose Your Adventurer',
        // No backgroundColor provided, so it will use the theme's primary color
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            fullWidthButtonWithImage(
              text: "Pirate",
              onPressed: () {
                _selectAdventure(context, 'Pirate');
              },
              imagePath:
                  'assets/images/pirate.jpeg', // Correct relative path to the image
              isDisabled: false, // Set to true if the button should be disabled
            ),
            SizedBox(height: 20),
            fullWidthButtonWithImage(
              text: "Medieval",
              onPressed: () {
                _selectAdventure(context, 'Medieval');
              },
              imagePath:
                  'assets/images/medieval.jpeg', // Correct relative path to the image
              isDisabled: false, // Set to true if the button should be disabled
            ),
            SizedBox(height: 20),
            fullWidthButtonWithImage(
              text: "Sci-Fi",
              onPressed: () {
                _selectAdventure(context, 'Sci-Fi');
              },
              imagePath:
                  'assets/images/sci-fi.jpeg', // Correct relative path to the image
              isDisabled: false, // Set to true if the button should be disabled
            ),
            SizedBox(height: 20),
            fullWidthButtonWithImage(
              text: "Fantasy",
              onPressed: () {
                _selectAdventure(context, 'Fantasy');
              },
              imagePath:
                  'assets/images/fantasy.jpeg', // Correct relative path to the image
              isDisabled: false, // Set to true if the button should be disabled
            ),
          ],
        ),
      ),
    );
  }
}
