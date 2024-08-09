import 'package:flutter/material.dart';
import 'common_widgets.dart';
import 'room_details_page.dart';

class AdventureTypePage extends StatelessWidget {
  void _selectAdventure(BuildContext context, String adventureType) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => RoomDetailsPage(),
      ),
    );
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
