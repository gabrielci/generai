// Scoresheet "class", in javascript you have to make an original object and then instantiate others by 
// making them inherit variables and methods with the "prototype" tag on the middle from this object or its
// children (That may themselves have more stuff to pass on)
(function(alseis, $, undefined) {
  // private members:
  
  // Bonus value added to score for getting certain plays on your first roll
  var first_shot_bonus = 5;
  
  // Object containing the base score for each play 
  var actual_scores = {
    '_4': 4,
    '_5': 5,
    '_6': 6,
    '_straight': 20,
    '_fullhouse': 30,
    '_four_of_a_kind': 40,
    '_yahtzee': 50
  };

  // Object containing the max score each play can give
  var max_scores = {
    '_4': actual_scores['_4'] * 5,
    '_5': actual_scores['_5'] * 5,
    '_6': actual_scores['_6'] * 5,
    '_straight': actual_scores['_straight'] + first_shot_bonus,
    '_fullhouse': actual_scores['_fullhouse'] + first_shot_bonus,
    '_four_of_a_kind': actual_scores['_four_of_a_kind'] + first_shot_bonus,
    '_yahtzee': actual_scores['_yahtzee'] + first_shot_bonus
  };

  // Method that returns the base score for a certain play (Does not consider the first_shot_bonus)
  var _single_score = function(play, val) {
    return val*actual_scores[play];
  };

  // Method that recieves the scoresheet number and player object and makes the Scoresheet object that contains:
  /*     notes: The score obtained on each score block on a sheet, initialy undefined (Or "empty") 
         no: The number of this particular Scoresheet on the whole array of scoresheets
         player: The player object (See game.js for more info)
         nnotes: The number of score blocks that are no longer undefined (A score has been jotted down on the block)
  */
  alseis.Scoresheet = function(no, player) {
    this.notes = {
      '_4': undefined,
      '_5': undefined,
      '_6': undefined,
      '_straight': undefined,
      '_fullhouse': undefined,
      '_four_of_a_kind': undefined,
      '_yahtzee': undefined
    };
    this.no = no;
    this.player = player;
    this.nnotes = 0;
  };

  // public methods

  // static
  // Method that returns the keyword used to select the color of the score box
  // (Primary = Blue, Success = Green, Warning = Yellow, Danger = Red)
  alseis.Scoresheet.GetColor = function (play, value, bonus) {
    console.log('play: ' + play + ' - value: ' + value);
    if (play == '_4' || play == '_5' || play == '_6') {
      var vv = value;
      if (vv >= 5)
        return 'primary';
      else if (vv >= 4)
        return 'success';
      else if (vv >= 2)
        return 'warning';
      else
        return 'danger';
    } else {
      if (value == 0)
        return 'danger';
      else if (bonus)
        return 'success';
      else
        return 'warning';
    }
  };


  // static
  // Method that maps an id to a corresponding play name
  alseis.Scoresheet.GetPlay = function (idx) {
    switch(idx) {
      case 0:
        return '_4';
      case 1:
        return '_5';
      case 2:
        return '_6';
      case 3:
        return '_straight';
      case 4:
        return '_fullhouse';
      case 5:
        return '_four_of_a_kind';
      case 6:
        return '_yahtzee';
    }
    return '';
  };

  // Takes note of a play, it increases the nnotes variable if the scoresheet box was empty (Undefined) and
  // writes the score with the bonus included on the box, then it sends the jquery event to modify the box
  alseis.Scoresheet.prototype.Note = function(play, val, bonus) {
    // TODO: add check for notes already commited?
    if (!this.notes[play]) this.nnotes++;
    this.notes[play] = val != -1 ? _single_score(play, val) + (bonus ? first_shot_bonus : 0) : undefined;
    $(this).trigger('score_changed', [this, play, val, bonus]);
  };
  /*OBSOLETE
  // Remove note from play
  alseis.Scoresheet.prototype.RemoveNote = function(play)
  {
    if (this.notes[play] !== undefined) this.nnotes--;
    this.notes[play] = undefined;
    $(this).trigger('score_changed', [this, play]);
  }
  */

  // Returns current score jotted down on the scoresheet "play" box (Remember that each particular scoresheet
  // is assigned to a player)
  var _current_score = function(play) {
    if (!notes[play])
      return undefined;
 
    return notes[play];
  }

  // Returns current cumulative score
  alseis.Scoresheet.prototype.CurrentScore = function() {
    var _current_score = 0;
    for (var p in this.notes) {
      if (this.notes.hasOwnProperty(p)) {
        _current_score += this.notes[p] ? this.notes[p] : 0;
      }
    }

    return _current_score;
  };

  /* Returns max possible score for the sheet*/
  alseis.Scoresheet.prototype.MaxScore = function() {
    var _max_score = 0;
    for (var p in this.notes) {
      if (this.notes.hasOwnProperty(p)) {
        _max_score += this.notes[p] != undefined ? this.notes[p] : max_scores[p];
      }
    }
    return _max_score;
  }

}( window.alseis = window.alseis || {}, jQuery ));


